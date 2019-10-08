import math

LIGHT_SPEED = 1


class Particle:
	""" Class describing a particle"""

	def __init__(self, name, mass, charge, momentum=0.):
		""" Arguments:
			- name of the particle
			- mass (in MeV/c^2)
			- charge (in e)
			- momentum [optional] in (MeV/c)
			"""
		self.name = name
		self._mass = mass
		self._charge = charge
		self.momentum = momentum

	def print_info(self):
		"""Print particle info in a nice, formatted way"""
		message = 'Particle "{}": '
		message += 'mass = {} MeV/c^2, charge = {} e, momentum = {}'
		print(message.format(self.name, self.mass,
							 self.charge, self.momentum))

	@property
	def charge(self):
		return self._charge

	@property
	def mass(self):
		return self._mass

	@property
	def momentum(self):
		return self._momentum

	@momentum.setter
	def momentum(self, value):
		if (value < 0):
			print('Cannot set the energy value inferior to zero')
			print('The momentum will be set to 0!')
			self._momentum = 0
		else:
			self._momentum = value

	@property
	def energy(self):
		return math.sqrt((self.momentum * LIGHT_SPEED) ** 2
						 + (self.mass * LIGHT_SPEED ** 2) ** 2)

	@energy.setter
	def energy(self, value):
		if (value < self.mass):
			print('Cannot set the energy value smaller '
				  'than its mass ({})!'.format(self.mass))
		else:
			self.momentum = (math.sqrt((value ** 2 -
									(self.mass * LIGHT_SPEED ** 2) ** 2))) / \
							LIGHT_SPEED ** 2

	@property
	def beta(self):
		if not (self.energy > 0.):
			return 0
		else:
			return LIGHT_SPEED * self.momentum/self.energy


	@beta.setter
	def beta(self, value):
		if (value < 0.) or (value >1.):
			print('Beta must be in the [0., 1.] range')
			return
		if (not (value < 1.) and (self.mass > 0)):
			print('Only massless particles can travel at Beta = 1!')
			return
		self.momentum = LIGHT_SPEED * value * self.mass / \
						math.sqrt(1 - value**2)

class Proton(Particle):
	"""Class describing a proton"""
	NAME = 'Proton'
	MASS = 938.272  # MeV/c^2
	CHARGE = +1

	def __init__(self, momentum=0.):
		# Particle.__init__(self, self.NAME, self.MASS, self.CHARGE, momentum)
		super().__init__(self.NAME, self.MASS, self.CHARGE, momentum)

class Alpha(Particle):
	"""Class describing an alpha nucleum"""
	NAME = 'Alpha'
	MASS = 3.7273e3 #MeV
	CHARGE = +4

	def __init__(self, momentum=0.):
		# Particle.__init__(self, self.NAME, self.MASS, self.CHARGE, momentum)
		super().__init__(self.NAME, self.MASS, self.CHARGE, momentum)


if __name__ == '__main__':
	particle = Particle('test_particle', mass=0.5, charge=2., momentum=100.)
	particle.print_info()
	print('Beta = {}'.format(particle.beta))
	particle.beta = -1
	particle.beta = 1
	particle.beta = 0.5
	# particle.charge = 3

	print('Proton:')
	proton = Proton(200.)
	proton.print_info()
	proton.beta = 0.8
	proton.print_info()

	print('Alpha particle:')
	alpha = Alpha(300)
	alpha.energy = 2000
