function twitterTijdlijn(query) {
	new TWTR.Widget({
	  version: 2,
	  type: 'search',
	  search: query,
	  interval: 2000,
	  subject: '',
	  width: 280,
	  height: 650,
	  theme: {
	    shell: {
	      background: 'transparent',
	      color: 'whitesmoke'
	    },
	    tweets: {
	      background: 'transparent',
	      color: 'whitesmoke'			    }
	  },
	  features: {
	    scrollbar: true,
	    loop: true,
	    live: true,
	    hashtags: true,
	    timestamp: true,
	    avatars: true,
	    behavior: 'all'
	  }
	}).render().start();
}