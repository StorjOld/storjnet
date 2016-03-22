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
    json.load(open("benchmark/filterupdates_quasar_size_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_f.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_g.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_h.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_i.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_j.json", "r")),
]


for sample in samples:

    # get x sub per min
    test_timedelta = sample["args"]["test_timedelta"]
    test_count = sample["args"]["test_count"]
    time_total = test_timedelta * test_count
    quasar_size = sample["quasar"]["constants"]["size"]
    x_amp.append(quasar_size)
    x_saturation.append(quasar_size)
    x_success.append(quasar_size)
    x_redundant.append(quasar_size)
    x_spam.append(quasar_size)

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
plot.set_title('Effect of subscription frequency on update call.')
plot.set_xlabel('Subscriptions / min')
plot.set_ylabel('%')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 600, 0, 100])


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
plt.savefig("benchmark/filterupdates_sub_freq_plot.png")
