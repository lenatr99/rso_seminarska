import matplotlib.pyplot as plt
import numpy as np

# Categories
labels = np.array(['Enostavnost uporabe', 'Fleksibilnost', 'Delovanje', 'Podpora skupnosti', 'State-of-the-Art zmogljivosti'])

# Ratings for each library
hugging_face = np.array([4, 4, 4, 5, 5])
gpt_neo = np.array([3, 4, 4, 3, 4])
fairseq = np.array([2, 5, 5, 4, 4])
tensorflow_gpt = np.array([3, 3, 4, 4, 3])

# Number of variables
num_vars = len(labels)

#change size of numbers on axes
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
# Compute angle each bar is centered on:
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# The plot is circular, so we need to "complete the loop" and append the start to the end.
hugging_face = np.concatenate((hugging_face, [hugging_face[0]]))
gpt_neo = np.concatenate((gpt_neo, [gpt_neo[0]]))
fairseq = np.concatenate((fairseq, [fairseq[0]]))
tensorflow_gpt = np.concatenate((tensorflow_gpt, [tensorflow_gpt[0]]))
angles += angles[:1]

# Plot
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
ax.fill(angles, hugging_face, color='red', alpha=0.2, edgecolor='red', linewidth=4)
ax.fill(angles, gpt_neo, color='blue', alpha=0.2, edgecolor='blue', linewidth=4)
ax.fill(angles, fairseq, color='green', alpha=0.2, edgecolor='green', linewidth=4)

#set border alpha as 1 to make it visible
ax.fill(angles, tensorflow_gpt, color='yellow', alpha=0.5, edgecolor='yellow', linewidth=4)


# Labels for each point
ax.set_xticks(angles[:-1])
#make sure they are outside the plot area
ax.set_xticklabels(labels, fontsize=15)

list1 = [0, 1, 4, 5] 
# Improve layout to avoid text overlapping
for i, (label, rot) in enumerate(zip(ax.get_xticklabels(), angles[:-1])):
    if i in list1:
        label.set_horizontalalignment("left")
    else:
        label.set_horizontalalignment("right")

# Legend
plt.legend(['Hugging Face', 'GPT-Neo', 'Fairseq', 'TensorFlow GPT'], loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=15)
plt.savefig('radar_plot.pdf', dpi=300, bbox_inches='tight')
