from mininet.topo import Topo

class testTopo( Topo ):

	def __init__( self ):
		#setLogLevel( 'info ' )
		# Initialize topology
		Topo.__init__(self)

		#info( '∗∗∗ Adding hosts\n' )
		h1 = self.addHost( 'h1', ip='10.0.0.10/22' )
		h2 = self.addHost( 'h2', ip='10.0.0.20/22' )
		h3 = self.addHost( 'h3', ip='10.0.0.30/22' )
		h4 = self.addHost( 'h4', ip='10.0.0.40/22' )
		h5 = self.addHost( 'h5', ip='10.0.0.50/22' )

		#info( '∗∗∗ Adding switches\n' )
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')

		#info( '∗∗∗ Creating links\n' )
		self.addLink( s1, s2, bw=10 )
		self.addLink( s1, s4, bw=10 )
		self.addLink( s2, s4, bw=10 )
		self.addLink( s3, s4, bw=10 )
		self.addLink( h1, s1, bw=10 )
		self.addLink( h2, s1, bw=10 )
		self.addLink( h3, s2, bw=10 )
		self.addLink( h4, s3, bw=10 )
		self.addLink( h5, s4, bw=10 )

topos = {'mytopo': (lambda: testTopo () ) }