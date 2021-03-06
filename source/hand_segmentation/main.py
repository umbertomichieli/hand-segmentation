# Custom
from data_generator import *
from network import *

# Paths
from os import path as op
import argparse

# Keras models
from keras import models

# %% Input parsing
# TODO: fix parser adding other inputs (e.g. learning rate, optimizer,...)
parser = argparse.ArgumentParser()

parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--batch_size", type=int, default=3)
parser.add_argument("--patience", type=int, default=10)

args = parser.parse_args()

epochs = args.epochs
batch_size = args.batch_size
patience = args.patience


# PATHS
project_root_path = op.relpath('../..')
data_root_path = op.join(project_root_path, 'data')
# features and labels paths
sets_root_path = op.join(data_root_path, 'sets')
features_path = op.join(sets_root_path, 'features.mat')
labels_path = op.join(sets_root_path, 'labels.mat')
# output model paths
save_model_dir = op.join(project_root_path, 'models')
save_model_path = op.join(save_model_dir, 'second_try.hdf5')

# Obtain data
features, labels = get_data(features_path, labels_path, reduce_images=False)
im_size = features.shape[1:4]

# Get model
model = get_unet_model(im_size)

# Compile
# As metrics we would like the pixel accuracy rather than the loss.
# Adam is ok, you might want to try other optimizers (e.g. SGD, Adagrad/Adadelta,...) and different learning rates.
# To specify the lr, need to create an optimizer object
model.compile(optimizer='adam', loss=bce_dice_loss, metrics=['accuracy'])

# Train
print("Ready to start training")
cp = tf.keras.callbacks.ModelCheckpoint(filepath=save_model_path, save_best_only=True, verbose=1)

# TODO: visualize learning via tensorboard (tensorboard --logdir 'tb/xxx' --port 6001)
callbacktb = tf.keras.callbacks.TensorBoard(log_dir="tb",
                         histogram_freq=0,
                         write_graph=True,
                         write_images=False)
                         #update_freq='batch')

# TODO: add restore_best_weights (maybe update to tf 1.13)
early_stop = tf.keras.callbacks.EarlyStopping(patience=patience,
                           min_delta=0)
                           #restore_best_weights=True)

callbacks = [callbacktb, early_stop, cp]

# I would suggest to split the data in advance and then use them always with the same split, for example:
'''model.fit(x=x_train,
      y=y_train,
      batch_size=train_batch_size,
      validation_data=(x_val, y_val),
      epochs=epochs,
      callbacks=callbacks)'''
model.fit(x=features,
          y=labels,
          batch_size=batch_size,
          epochs=epochs,
          verbose=2,
          callbacks=callbacks,
          validation_split=0.2)

# %% TODO: Evaluate performance  (sample code to modify)
#y_hat = m.predict(x_test)

#m.save(path.join(save_path, "model.h5"))
# np.save(path.join(savepath, "history"), history)
#np.save(path.join(save_path, "y_hat"), y_hat)
#utils.write_results(y_true=y_test,
#                    y_pred=y_hat,
#                    filepath=path.join(save_path, "results.txt"))


# %%
# TODO: sanity check on losses (I had negative values)
# TODO: compare results using CE, CE+dice, dice
# TODO: generate more data (maybe then need to use a data generator which does not load all the images in RAM at once)
#  --> maybe we ask professor about source code

# TODO: compute per class pixel accuracy, per class IoU, mean IoU, mean PA, mean class accuracy (using provided file)


