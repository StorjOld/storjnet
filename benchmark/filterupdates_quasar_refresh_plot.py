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
    json.load(open("benchmark/filterupdates_quasar_refresh_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_f.json", "r")),
#   json.load(open("benchmark/filterupdates_quasar_refresh_g.json", "r")),
#   json.load(open("benchmark/filterupdates_quasar_refresh_h.json", "r")),
#   json.load(open("benchmark/filterupdates_quasar_refresh_i.json", "r")),
#   json.load(open("benchmark/filterupdates_quasar_refresh_j.json", "r")),
]


for sample in samples:

    # get x sub per min
    test_timedelta = sample["args"]["test_timedelta"]
    test_count = sample["args"]["test_count"]
    time_total = test_timedelta * test_count
    refresh_time = sample["quasar"]["constants"]["refresh_time"]
    x_amp.append(refresh_time)
    x_saturation.append(refresh_time)
    x_success.append(refresh_time)
    x_redundant.append(refresh_time)
    x_spam.append(refresh_time)

    # get saturation percent
    ksize = 20
    update_called = sample["quasar"]["update_called"]
    num_refreshes = time_total / sample["quasar"]["constants"]["refresh_time"]
    swarm_size = sample["args"]["swarm_size"]
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
plot.set_title('Effect of quasar refresh time on update call.')
plot.set_xlabel('Refresh time in sec.')
plot.set_ylabel('%')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 100, 0, 100])


# add plots
lines = plot.plot(x_success, y_success, 'k', label='Update success %')
plt.setp(lines, color='green', linewidth=2.0)
lines = plot.plot(x_redundant, y_redundant, 'k', label='Update redundant %')
plt.setp(lines, color='orange', linewidth=2.0)
lines = plot.plot(x_spam, y_spam, 'k', label='Update spam %')
plt.setp(lines, color='red', linewidth=2.0)
lines = plot.plot(x_saturation, y_saturation, 'k', label='Saturation %')
plt.setp(lines, color='blue', linewidth=2.0)


# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')

# render
plt.savefig("benchmark/filterupdates_quasar_refresh_plot.png")
