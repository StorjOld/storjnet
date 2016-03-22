# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt  # pip install matplotlib
import json


x_amp = []
y_amp = []
x_saturation = []
y_saturation = []
x_success = []
y_success = []
x_redundant = []
y_redundant = []
x_spam = []
y_spam = []


samples = [
    json.load(open("benchmark/filterupdates_quasar_extraprop_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_f.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_g.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_h.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_i.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_j.json", "r")),
]


for sample in samples:

    # get x sub per min
    test_timedelta = sample["args"]["test_timedelta"]
    test_count = sample["args"]["test_count"]
    time_total = test_timedelta * test_count
    extra_propagations = sample["quasar"]["constants"]["extra_propagations"]
    x_amp.append(extra_propagations)
    x_saturation.append(extra_propagations)
    x_success.append(extra_propagations)
    x_redundant.append(extra_propagations)
    x_spam.append(extra_propagations)

    # get y amp percent
    ksize = 20
    max_amp = ksize ** sample["quasar"]["constants"]["depth"]
    update_called = sample["quasar"]["update_called"]
    num_refreshes = time_total / sample["quasar"]["constants"]["refresh_time"]
    swarm_size = sample["args"]["swarm_size"]
    amp = update_called / (test_count + (num_refreshes * swarm_size))
    amp_percent = amp * 100.0 / max_amp
    y_amp.append(amp_percent)

    # get saturation percent
    extra_propagations = sample["quasar"]["constants"]["extra_propagations"]
    max_node_updates = num_refreshes * (extra_propagations + 1)
    max_called = swarm_size * max_node_updates * ksize  # ~ 880000
    saturation_percent = update_called * 100 / max_called
    y_saturation.append(saturation_percent)

    # get success precent
    success_count = sample["quasar"]["update_successful"]
    success_percent = success_count * 100.0 / update_called
    y_success.append(success_percent)

    # get redundant precent
    redundant_count = sample["quasar"]["update_redundant"]
    redundant_percent = redundant_count * 100.0 / update_called
    y_redundant.append(redundant_percent)

    # get spam precent
    spam_count = sample["quasar"]["update_spam"]
    spam_percent = spam_count * 100.0 / update_called
    y_spam.append(spam_percent)


# setup plot
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_title('Effect of quasar extra propagations on update call.')
plot.set_xlabel('Extra propagations')
plot.set_ylabel('%')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 20, 0, 100])


# add plots
lines = plot.plot(x_success, y_success, 'k', label='Update success %')
plt.setp(lines, color='green', linewidth=2.0)
lines = plot.plot(x_redundant, y_redundant, 'k', label='Update redundant %')
plt.setp(lines, color='orange', linewidth=2.0)
lines = plot.plot(x_spam, y_spam, 'k', label='Update spam %')
plt.setp(lines, color='red', linewidth=2.0)
lines = plot.plot(x_amp, y_amp, 'k', label='Amplification %')
plt.setp(lines, color='pink', linewidth=2.0)
lines = plot.plot(x_saturation, y_saturation, 'k', label='Saturation %')
plt.setp(lines, color='blue', linewidth=2.0)


# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')

# render
plt.savefig("benchmark/filterupdates_quasar_extraprop_plot.png")
