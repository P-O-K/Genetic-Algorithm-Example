
from random import randint, choice, uniform
from sys import setrecursionlimit; setrecursionlimit = 500

class Agent( object ):
	"""docstring for Agent"""

	STRUCTURE :str
	FITNESS :int
	__index :int

	def __init__( self, structure:str, fitness:int ):
		super( Agent, self ).__init__( )
		self.STRUCTURE = structure
		self.FITNESS = fitness


	def __repr__( self ) -> str:
		return f'{self.STRUCTURE} | FIT: {self.FITNESS}'


	def __str__( self ) -> str:
		return f'{self.STRUCTURE} | FIT: {self.FITNESS}'


	def __iter__( self ):
		self.__index = 0
		return self


	def __next__( self ) -> chr:
		if self.__index < len( self.STRUCTURE ):
			self.__index +=1
			return self.STRUCTURE[ self.__index -1 ]

		else:
			raise StopIteration


	def __eq__( self, other ):
		return self.STRUCTURE == other.STRUCTURE



class GeneticAlgorithm( object ):
	"""docstring for GeneticAlgorithm"""


	TARGET :str = 'Genetic <&%@?|/> Algorithm'

	MIN_BASE_VALUE :int = 32
	MAX_BASE_VALUE :int = 126

	GENERATION :list = list( )
	TOP_AGENT :Agent = Agent( '', 0 )
	COUNT :int = 0


	def __init__( self, populationSize:int, groupingSizePCT:float, mutationRatePCT:float, coincidencePCT:float ):
		super( GeneticAlgorithm, self ).__init__( )

		self.populationSize = populationSize
		self.groupingSizePCT = groupingSizePCT
		self.mutationRatePCT = mutationRatePCT
		self.coincidencePCT = coincidencePCT
		self.matingPoolSize = int( self.populationSize -int( self.populationSize *self.groupingSizePCT ) )

		self.assembleGeneration( )



	# Tops of current generation to fill population quota
	def assembleGeneration( self ) -> None:
		while len( self.GENERATION ) < self.populationSize:
			string = ''.join( chr( self.sampleMutations( self.MIN_BASE_VALUE, self.MAX_BASE_VALUE )  ) for _ in range( len( self.TARGET ) ) )
			self.GENERATION.append( Agent( string, self.evaluateFitness( string, self.TARGET ) ) )



	def crossover( self, agentOne:Agent, agentTwo:Agent ) -> str:
		string = str( )
		for a1, a2 in zip( agentOne, agentTwo ):
			if uniform( 0, 1 ) <= self.mutationRatePCT +( -self.coincidencePCT if a1==a2 else self.coincidencePCT ):
				string += chr( self.sampleMutations( self.MIN_BASE_VALUE, self.MAX_BASE_VALUE ) )
			else:
				string += choice( ( a1, a2 ) )

		return string



	def procreate( self ) -> None:
		nextGeneration = list( )
		while len( nextGeneration ) < self.matingPoolSize:

			agentOne, agentTwo = self.pickParentAgent( ), self.pickParentAgent( )
			if agentOne == agentTwo: continue

			string:str = self.crossover( agentOne, agentTwo )
			newAgent = Agent( string, self.evaluateFitness( string, self.TARGET ) )
			
			nextGeneration.append( newAgent )
			if newAgent.FITNESS >= self.TOP_AGENT.FITNESS: self.TOP_AGENT = newAgent

		self.GENERATION = nextGeneration
		self.COUNT +=1
		self.assembleGeneration( )



	def pickParentAgent( self ) -> tuple( ( Agent, Agent ) ):
		agent = choice( self.GENERATION )
		if 2**agent.FITNESS >= randint( 0, 2**self.TOP_AGENT.FITNESS ): return agent

		try: return self.pickParentAgent( )
		except RecursionError: return agent #Recursion limit exceeded



	@staticmethod
	def getGenerationAverage( generation:list ) -> int:
		return sum( [ agent.FITNESS for agent in generation ] ) /len( generation )



	@staticmethod
	def sampleMutations( MIN_BASE:int, MAX_BASE:int ) -> int:
		return randint( MIN_BASE, MAX_BASE )



	@staticmethod
	def evaluateFitness( string:str, target:str ) -> int:
		return sum( [ st==ta for st,ta in zip( string, target ) ] )



	@staticmethod
	def progressReport( currentIteration:int, maxIteration:int, percentInterrupt:int ) -> bool:
		if currentIteration %int( ( maxIteration /100 ) *percentInterrupt ) == 0:
			print( f'Progress Update: { currentIteration /maxIteration :.1%}' )
			return True
		return False



if __name__ == '__main__':
	GA = GeneticAlgorithm( populationSize=100, groupingSizePCT=0.15, mutationRatePCT=.12, coincidencePCT=0.02 )

	safetyNet = 500
	while( GA.TOP_AGENT.STRUCTURE != GA.TARGET ) and ( GA.COUNT < safetyNet ):
		GA.procreate( )

		if GA.progressReport( GA.COUNT, safetyNet, 20 ):
			print( f'\tGEN: {GA.COUNT :0>3d} -> {GA.TOP_AGENT} -> AVG: {GA.getGenerationAverage( GA.GENERATION ) :.2f}' )


	print( '\nSimulation Complete:' )
	print( f'Generations: {GA.COUNT}' )
	print( f'Best Agent: {GA.TOP_AGENT}' )
