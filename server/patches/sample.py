""" A monkey patch for the sample_sequence function of gpt-2-simple """
import tensorflow as tf
from gpt_2_simple.src import model

def sample_sequence(*, hparams, context=None, temperature=1):

    assert context is not None, 'Specify exactly one of start_token and context!'

    def predict(hparams, tokens):
        lm_output = model.model(hparams=hparams, X=tokens,
                                reuse=tf.compat.v1.AUTO_REUSE)

        logits = lm_output['logits'][:, :, :hparams.n_vocab]

        return logits

    with tf.compat.v1.name_scope('sample_sequence'):

        context_output = predict(hparams, context)
        logits = context_output[:, -1, :] / tf.cast(temperature, tf.float32)

        return tf.nn.softmax(logits)[0]
