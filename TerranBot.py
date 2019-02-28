import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, BARRACKS, MARINE, FACTORY, SIEGETANK
import random



class TerranBot(sc2.BotAI):
	async def on_step(self, iteration):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depots()
		await self.build_refinery()
		await self.expand()
		await self.build_barracks()
		await self.build_factory()
		await self.train_marines()
		await self.attack()

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
		if self.units(COMMANDCENTER).amount < 4 and self.can_afford(COMMANDCENTER):
			await self.expand_now()

	async def build_barracks(self):
		if self.units(SUPPLYDEPOT).ready.exists:
			supplydepot = self.units(SUPPLYDEPOT).ready.random
			if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
				await self.build(BARRACKS, near=supplydepot)

	async def build_factory(self):
		if self.units(BARRACKS).ready.exists:
			barracks = self.units(BARRACKS).ready.random
			if self.can_afford(FACTORY) and not self.already_pending(FACTORY):
				await self.build(FACTORY, near=barracks)

	async def train_marines(self):
		for barracks in self.units(BARRACKS).ready.noqueue:
			if self.can_afford(MARINE) and self.supply_left > 0:
				await self.do(barracks.train(MARINE))

	def find_target(self, state):
		if len(self.known_enemy_units) > 0:
			return random.choice(self.known_enemy_units)
		elif len(self.known_enemy_structures) > 0:
			return random.choice(self.known_enemy_structures)
		else:
			return self.enemy_start_locations[0]


	async def attack(self):
		if self.units(MARINE).amount > 60:
			for marine in self.units(MARINE).idle:
				await self.do(marine.attack(self.find_target(self.state)))

		elif self.units(MARINE). amount > 3:
			if len(self.known_enemy_units) >0:
				for marine in self.units(MARINE).idle:
					await self.do(marine.attack(random.choice(self.known_enemy_units)))			






run_game(maps.get("AbyssalReefLE"), [
	Bot(Race.Terran, TerranBot()),
	Computer(Race.Terran, Difficulty.Hard)
	], realtime=False)