
from random import randint, choice, uniform
from sys import setrecursionlimit; setrecursionlimit = 500

class Agent( object ):

	STRUCTURE :list
	FITNESS :int
	__index :int


	getChrString = lambda self: ''.join( chr( i ) if i>31 and i<127 else '█' for i in self.STRUCTURE )
								 	    # ↑ ALT code 219


	def __init__( self, structure:list, fitness:int ) -> None:
		'''structure: Takes in an array of numbers'''
		super( Agent, self ).__init__( )
		self.STRUCTURE = structure
		self.FITNESS = fitness



	def __str__( self ) -> str:
		return f'{self.STRUCTURE} -> {self.FITNESS}'



	def __iter__( self ) -> object:
		self.__index = 0
		return self



	def __next__( self ) -> chr:
		if self.__index < len( self.STRUCTURE ):
			self.__index += 1
			return self.STRUCTURE[ self.__index -1 ]

		raise StopIteration



	def __eq__( self, other ):
		return self.STRUCTURE == other.STRUCTURE




class GeneticAlgorithm( object ):


	TARGET :Agent = Agent( [ ord( i ) for i in '<~G3n3tic A!g0rithm:$@mple~>' ], 0 )

	GENERATION = list( )
	TOP_AGENT = Agent( list( ), 0 )

	MIN_BASE_VALUE :int = 0
	MAX_BASE_VALUE :int = 255
	MAX_ALTR_VALUE :int = 5

	GEN_COUNT :int = 1


	def __init__( self, populationSize:int, packSizePCT:float, mutationRatePCT:float, coincidencePCT:float ) -> None:
		self.populationSize = populationSize
		self.packSizePCT = packSizePCT
		self.mutationRatePCT = mutationRatePCT
		self.coincidencePCT = coincidencePCT
		self.matingPoolSize = self.populationSize *( 1 -self.packSizePCT  )

		self.fillGeneration( )



	def fillGeneration( self ) -> None:
		'''Fills the GENERATION array with random Agents from len( GENERATION ) up to self.populationSize'''
		while len( self.GENERATION ) < self.populationSize:
			newStructure = [ self.sampleMutations( self.MIN_BASE_VALUE, self.MAX_BASE_VALUE ) for _ in range( len( self.TARGET.STRUCTURE ) ) ]
			self.GENERATION.append( Agent( newStructure, self.evaluateFitness( newStructure, self.TARGET.STRUCTURE ) ) )
	


	def crossover( self, agentOne:Agent, agentTwo:Agent ) -> list:
		newStructure = list( )
		for a1, a2 in zip( agentOne, agentTwo ):
			if uniform( 0, 1 ) <= self.mutationRatePCT +( -self.coincidencePCT if a1==a2 else self.coincidencePCT ):
				newStructure.append( self.sampleMutations( self.MIN_BASE_VALUE, self.MAX_BASE_VALUE ) )
			else:
				newStructure.append( choice( ( a1, a2 ) ) )

		return newStructure



	def procreate( self ) -> None:
		nextGeneration = list( )
		while len( nextGeneration ) < self.matingPoolSize:
			agentOne, agentTwo = self.pickParentAgent( ), self.pickParentAgent( )
			if agentOne == agentTwo: continue

			newStructure = self.crossover( agentOne, agentTwo )
			newAgent = Agent( newStructure, self.evaluateFitness( newStructure, self.TARGET.STRUCTURE ) )
			nextGeneration.append( newAgent )

			if newAgent.FITNESS >= self.TOP_AGENT.FITNESS: self.TOP_AGENT = newAgent

		self.GENERATION = nextGeneration
		self.fillGeneration( )
		self.GEN_COUNT += 1



	def pickParentAgent( self ) -> Agent:
		agent = choice( self.GENERATION )
		if 2**agent.FITNESS >= randint( 0, 2**self.TOP_AGENT.FITNESS ): return agent

		try: return self.pickParentAgent( )
		except RecursionError: return agent #Recursion limit exceeded: Safety Catch



	@staticmethod
	def sampleMutations( MIN_BASE:int, MAX_BASE:int ) -> int :
		return randint( MIN_BASE, MAX_BASE )



	@staticmethod
	def evaluateFitness( nStructure:list, tStructure:list ) -> int:
		return sum( [ n==t for n,t in zip( nStructure, tStructure ) ] )



	@staticmethod
	def alterValue( value:int, MAX_ALTR:int ) -> int:
		return value +randint( -MAX_ALTR, MAX_ALTR )



	@staticmethod
	def generationAverage( generation:list ) -> float:
		return sum( [ agent.FITNESS for agent in generation ] ) /len( generation )



	@staticmethod
	def progressReport( currentIteration:int, maxIteration:int, percentInterrupt:int ) -> bool:
		if currentIteration %int( ( maxIteration /100 ) *percentInterrupt ) == 0:
			print( f'Progress Update: { currentIteration /maxIteration :.1%}' )
			return True
		return False




if __name__ == '__main__':
	GA = GeneticAlgorithm( populationSize=100, packSizePCT=0.15, mutationRatePCT=.12, coincidencePCT=0.02 )
	safetyNet = 500

	print( f'\tGEN: {GA.GEN_COUNT :0>3d} -> {None} -> AVG: {GA.generationAverage( GA.GENERATION )}\n' )
	while( GA.TOP_AGENT != GA.TARGET ) and ( GA.GEN_COUNT < safetyNet ):
		GA.procreate( )

		if GA.progressReport( GA.GEN_COUNT, safetyNet, 10 ):
			print( f'\tGEN: {GA.GEN_COUNT :0>3d} -> {GA.TOP_AGENT.getChrString( )} -> {GA.TOP_AGENT.FITNESS}\n\t\t{GA.TOP_AGENT}\n' )


	print( '\nSimulation Complete:' )
	print( f'\tTotal Generations: {GA.GEN_COUNT}' )
	print( f'\tTop Agent: {GA.TOP_AGENT.getChrString( )}, \n\t\t{GA.TOP_AGENT}' )
