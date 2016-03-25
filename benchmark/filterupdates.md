# Testing Strategy

First run quick limited tests to find out what to test extensivly.


### Mesurements

 * filter update called
 * filter update successful (filters updated and maybe propagated)
 * filter update redundant (filters not updated)
 * filter update spam (call from a peer that is not a neighbor)



## Test quasar refresh rate

Test what effect different quasar refresh rates have.
Subscriptions are to random topics from random nodes.

### Constants:

 * swarm size: 400 (theoretical maximum amplification)
 * quasar depth: 2 (limit full cascade to max 400 nodes)
 * quasar ttl: 64
 * quasar extra propagations: 10
 * test timedelta: 0.125
 * test count: 4800
 * quasar size: 512
 * subscription entropy: 256bit

### Varibles:

 * quasar refresh time
 * quasar freshness: quasar refresh time + 6

### Results:

![Plot](filterupdates_push/quasar_refresh_plot.png)

### Interpretation / Observations

A larger refresh interval reduces spam as each update call has a higher
likelyhood of introducing meaningfull changes.

In the intrest of spam reduction the largest practical refresh interval
should be chosen.



## Test subscription entropy

### Constants:

 * swarm size: 400 (theoretical maximum amplification)
 * quasar depth: 2 (limit full cascade to max 400 nodes)
 * quasar ttl: 64
 * quasar freshness: 66 (1min 6sec)
 * quasar refresh time: 60 (1min to fit in 10min test timeframe)
 * quasar extra propagations: 10
 * test timedelta: 0.125
 * test count: 4800
 * quasar size: 512

### Varibles:

 * subscription entropy

### Results:

![Plot](filterupdates_push/sub_entropy_plot.png)

### Interpretation / Observations

The lower the subscription entropy the less updates are propagated, as the
chance the neighboring node already has the entry is higher.

With increased subscription entropy the updates increase until it is limited
by the quasar refresh rate.


## Test quasar extra propagations

Test what effect different quasar extra propagations have.
Subscriptions are to random topics from random nodes.

### Constants:

 * swarm size: 400 (theoretical maximum amplification)
 * quasar depth: 2 (limit full cascade to max 400 nodes)
 * quasar ttl: 64
 * quasar freshness: 66 (1min 6sec)
 * quasar refresh time: 60 (1min to fit in 10min test timeframe)
 * test timedelta: 2
 * test count: 300
 * quasar size: 512
 * subscription entropy: 256bit

### Varibles:

 * quasar extra propagations

### Results:

![Plot](filterupdates_push/quasar_extraprop_plot.png)

### Interpretation / Observations

Initially increased extra propagations increased the update rate as expected.

However it peaked at 8-10 extra propagations,
this is the limit of the test setup in general.



## Test subscription frequency

### Constants:

 * swarm size: 400 (theoretical maximum amplification)
 * quasar size: 512 (largest possable for net rpc transfer)
 * quasar depth: 2 (limit full cascade to max 400 nodes)
 * quasar ttl: 64
 * quasar freshness: 66 (1min 6sec)
 * quasar refresh time: 60 (1min to fit in 10min test timeframe)
 * quasar extra propagations: 10
 * subscription entropy: 256bit

### Varibles:

 * test timedelta
 * test count


### Results:

![Plot](filterupdates_push/sub_freq_plot.png)

### Interpretation / Observations

The rate of subscriptions has little overall effect. This is mainly due to
the quasar refresh rate and extra propagations being the limiting factors.



## Test quasar bloom filter size

### Constants:

 * swarm size: 400 (theoretical maximum amplification)
 * quasar depth: 2 (limit full cascade to max 400 nodes)
 * quasar ttl: 64
 * quasar freshness: 66 (1min 6sec)
 * quasar refresh time: 60 (1min to fit in 10min test timeframe)
 * quasar extra propagations: 10
 * test timedelta: 0.125
 * test count: 4800
 * subscription entropy: 256bit

### Varibles:

 * quasar size

### Results:

![Plot](filterupdates_push/quasar_size_plot.png)

### Interpretation / Observations

The tested subscription rate is not enough to saturate the quasar attenuated
bloom filters?
