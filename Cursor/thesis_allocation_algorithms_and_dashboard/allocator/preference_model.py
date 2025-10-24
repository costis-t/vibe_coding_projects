from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from .entities import Student, Topic


class PreferenceModelConfig:
    def __init__(
        self,
        allow_unranked: bool = True,
        tier2_cost: int = 1,
        tier3_cost: int = 5,
        unranked_cost: int = 200,
        top2_bias: bool = True
    ):
        self.allow_unranked = allow_unranked
        self.tier2_cost = tier2_cost
        self.tier3_cost = tier3_cost
        self.unranked_cost = unranked_cost
        self.top2_bias = top2_bias


class PreferenceModel:
    """
    Computes edge costs per (student, topic).
    Precedence: overrides > tiers > ranks > unranked; banned => no edge.
    """

    def __init__(self, topics: Dict[str, Topic], overrides: Dict[Tuple[str, str], int] | None, cfg: PreferenceModelConfig):
        self.topics = topics
        self.overrides = overrides or {}
        self.cfg = cfg

    def _rank_cost(self, rank: int) -> int:
        if self.cfg.top2_bias:
            if rank == 1: return 0
            if rank == 2: return 1
            return 100 + (rank - 3)
        else:
            return rank - 1

    def compute_costs(self, students: Dict[str, Student]) -> Dict[Tuple[str, str], int]:
        costs: Dict[Tuple[str, str], int] = {}
        topic_ids = list(self.topics.keys())

        for student, s in students.items():
            if not s.plan:
                continue

            # NEW: forced_topic takes absolute precedence
            if s.forced_topic:
                if s.forced_topic in topic_ids and s.forced_topic not in s.banned:
                    costs[(student, s.forced_topic)] = -10000  # Very high priority (large negative cost = maximize this)
                continue

            # quick lookup
            rank_index = {t: i+1 for i, t in enumerate(s.ranks)} if s.ranks else {}

            for tid in topic_ids:
                # banned -> skip
                if tid in s.banned:
                    continue
                # override
                if (student, tid) in self.overrides:
                    costs[(student, tid)] = self.overrides[(student, tid)]
                    continue

                # tiers
                if s.tiers:
                    if tid in s.tiers.get(1, []):
                        costs[(student, tid)] = 0
                        continue
                    if tid in s.tiers.get(2, []):
                        costs[(student, tid)] = self.cfg.tier2_cost
                        continue
                    if tid in s.tiers.get(3, []):
                        costs[(student, tid)] = self.cfg.tier3_cost
                        continue

                # ranks
                if tid in rank_index:
                    costs[(student, tid)] = self._rank_cost(rank_index[tid])
                    continue

                # unranked fallback
                if self.cfg.allow_unranked:
                    costs[(student, tid)] = self.cfg.unranked_cost
                # else: no edge

        return costs

    @staticmethod
    def derive_preference_rank(student: Student, topic_id: str) -> int:
        """
        For reporting (non-colliding values):
          - forced: -1
          - tiers: 0 (tier1), 1 (tier2), 2 (tier3)
          - ranks: 10 (1st), 11 (2nd), 12 (3rd), 13 (4th), 14 (5th)
          - unranked: 999
        """
        if student.forced_topic and topic_id == student.forced_topic:
            return -1
        if student.tiers:
            if topic_id in student.tiers.get(1, []): return 0
            if topic_id in student.tiers.get(2, []): return 1
            if topic_id in student.tiers.get(3, []): return 2
        if topic_id in student.ranks:
            rank_idx = student.ranks.index(topic_id) + 1
            return 9 + rank_idx  # 10, 11, 12, 13, 14
        return 999
