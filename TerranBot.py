import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT



class TerranBot(sc2.BotAI):
	async def on_step(self, iteration):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depots()

	async def build_workers(self):
		for commandcenter in self.units(COMMANDCENTER).ready.noqueue:
			if self.can_afford(SCV):
				await self.do(commandcenter.train(SCV))	

	async def build_supply_depots(self):
		if self.supply_left < 5 and not self.already_pending(SUPPLYDEPOT):
			commandcenters = self.units(COMMANDCENTER).ready
			if commandcenters.exists:
				if self.can_afford(SUPPLYDEPOT):
					await self.build(SUPPLYDEPOT, near=commandcenters.first)			




run_game(maps.get("AbyssalReefLE"), [
	Bot(Race.Terran, TerranBot()),
	Computer(Race.Terran, Difficulty.Easy)
	], realtime=False)