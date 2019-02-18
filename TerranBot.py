import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, BARRACKS



class TerranBot(sc2.BotAI):
	async def on_step(self, iteration):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depots()
		await self.build_refinery()
		await self.expand()
		await self.build_barracks()

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

	async def build_refinery(self):
		for commandcenter in self.units(COMMANDCENTER).ready:
			geysers = self.state.vespene_geyser.closer_than(15.0, commandcenter)
			for geyser in geysers:
				if not self.can_afford(REFINERY):
					break
				worker = self.select_build_worker(geyser.position)
				if worker is None:
					break
				if not self.units(REFINERY).closer_than(1.0, geyser).exists:
					await self.do(worker.build(REFINERY, geyser))

	async def expand(self):
		if self.units(COMMANDCENTER).amount < 3 and self.can_afford(COMMANDCENTER):
			await self.expand_now()

	async def build_barracks(self):
		if self.units(SUPPLYDEPOT).ready.exists:
			supplydepot = self.units(SUPPLYDEPOT).ready.random
			if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
				await self.build(BARRACKS, near=supplydepot)








run_game(maps.get("AbyssalReefLE"), [
	Bot(Race.Terran, TerranBot()),
	Computer(Race.Terran, Difficulty.Easy)
	], realtime=False)