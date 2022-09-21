class ANOVA:
    def __init__(self, data):
        self.data = data.to_list()
        self.data_size = len(self.data)
        pass
    def get_observation(self,stepsize=3):
        step = stepsize
        slopes = []
        for i in range(self.data_size- step):
            cur = input[i + step]
            prev = input[i]
            slope = (cur - prev) / step
            slopes.append(slope)
        return slopes

    def run(self):
        obs = self.get_observation()
        