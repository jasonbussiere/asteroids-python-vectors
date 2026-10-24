class ColisionDetection:
    def resolve_group_colisions(self, group_a, group_b):
        for a in group_a:
            for b in group_b:
                #only check colisions if both are still alive!
                if a.is_alive() and b.is_alive():
                    if a.has_collided_with(b):
                        a.on_impact_with(b)
                        b.on_impact_with(a)