import tensorflow as tf
import numpy as np
import os
import logging
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#logging.getLogger('tensorflow').setLevel(logging.ERROR)



def split_input_target(chunk):
  input_text = chunk[:-1]
  target_text = chunk[1:]
  return input_text, target_text


def generate_text(model, char2idx, idx2char, num_generate, temperature, start_string ):
  input_eval = [char2idx[s] for s in start_string] # string to numbers (vectorizing)
  input_eval = tf.expand_dims(input_eval, 0) # dimension expansion
  text_generated = [] # Empty string to store our results
  model.reset_states() # Clears the hidden states in the RNN

  sentence_counter = 0
  max_sentences = random.randint(2, 5)
  max_len = 500

  while sentence_counter < max_sentences : #Run a loop for number of characters to generate
    predictions = model(input_eval) # prediction for single character
    predictions = tf.squeeze(predictions, 0) # remove the batch dimension

    if len(text_generated) > max_len: 
       break

    # using a categorical distribution to predict the character returned by the model
    # higher temperature increases the probability of selecting a less likely character
    # lower --> more predictable
    predictions = predictions / temperature
    predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

    # The predicted character as the next input to the model
    # along with the previous hidden state
    # So the model makes the next prediction based on the previous character
    input_eval = tf.expand_dims([predicted_id], 0)
    # Also devectorize the number and add to the generated text

    new_char = idx2char[predicted_id]

    if new_char == '.':
      sentence_counter += 1
    


    text_generated.append(new_char)

    st = ''.join(a for a in text_generated)
    print(st)
    print('--------------------------------')
  return (start_string + ''.join(text_generated))

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
  model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim,
                              batch_input_shape=[batch_size, None]),
    tf.keras.layers.GRU(rnn_units,
                        return_sequences=True,
                        stateful=True,
                        recurrent_initializer='glorot_uniform'),
    tf.keras.layers.Dense(vocab_size)
  ])
  return model


def loss(labels, logits):
  return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

path_to_file = tf.keras.utils.get_file('sample.txt',
                                       'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')


import os


def init_search(user_request):
  # assign directory
  directory = 'dataset'

  ite = 0

  # iterate over files in
  # that directory
  for filename in os.listdir(directory):
      print('Opening: ', filename)
      f = os.path.join(directory, filename)
      # checking if it is a file
      if os.path.isfile(f):
          ite += 1
          if ite == 1:
              text = open('dataset/' + filename, 'rb').read()
          else:
              anime_text = open('dataset/' + filename, 'rb').read()
              text += anime_text

  # Read, then decode for py2 compat.
  text = text.decode(encoding='utf-8')
  print ('Total number of characters in the corpus is:', len(text))
  print('The first 100 characters of the corpus are as follows:\n', text[:100])


  # The unique characters in the corpus
  vocab = sorted(set(text))
  print ('The number of unique characters in the corpus is', len(vocab))
  print('A slice of the unique characters set:\n', vocab[:10])

  # Create a mapping from unique characters to indices
  char2idx = {u:i for i, u in enumerate(vocab)}
  # Make a copy of the unique set elements in NumPy array format for later use in the decoding the predictions
  idx2char = np.array(vocab)
  # Vectorize the text with a for loop
  text_as_int = np.array([char2idx[c] for c in text])

  # Create training examples / targets
  char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
  # for i in char_dataset.take(5):
  #   print(i.numpy())
  seq_length = 250 # The max. length for single input
  # examples_per_epoch = len(text)//(seq_length+1) # double-slash for “floor” division
  sequences = char_dataset.batch(seq_length+1, drop_remainder=True)
  # for item in sequences.take(5):
  #   print(repr(''.join(idx2char[item.numpy()])))


  dataset = sequences.map(split_input_target)

  print(dataset)

  BUFFER_SIZE = 10000 # TF shuffles the data only within buffers

  BATCH_SIZE = 512 # Batch size

  dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

  print(dataset)

  # Length of the vocabulary in chars
  vocab_size = len(vocab)
  # The embedding dimension
  embedding_dim = 256
  # Number of RNN units
  rnn_units = 1024


  model = build_model(
      vocab_size = len(vocab), # no. of unique characters
      embedding_dim=embedding_dim, # 256
      rnn_units=rnn_units, # 1024
      batch_size=BATCH_SIZE)  # 64 for the traning

  model.summary()


  model.compile(optimizer='adam', loss=loss)

  # Directory where the checkpoints will be saved
  checkpoint_dir = './training_checkpoints'
  # Name of the checkpoint files
  checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

  checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
      filepath=checkpoint_prefix,
      save_weights_only=True)

  model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)
  model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
  model.build(tf.TensorShape([1, None]))

  token = user_request
  return generate_text(
                      model,
                      char2idx,
                      idx2char,
                      num_generate=1000,
                      temperature=0.45,
                      start_string=token,
                      )
