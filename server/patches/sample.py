""" A monkey patch for the sample_sequence function of gpt-2-simple """
import tensorflow as tf

import time

from gpt_2_simple.src import model

# def top_k_logits(logits, k):
#     if k == 0:
#         # no truncation
#         return logits
#
#     def _top_k():
#         values, _ = tf.nn.top_k(logits, k=k)
#         min_values = values[:, -1, tf.newaxis]
#         return tf.compat.v1.where(
#             logits < min_values,
#             tf.ones_like(logits, dtype=logits.dtype) * -1e10,
#             logits,
#         )
#     return tf.cond(
#         pred=tf.equal(k, 0),
#         true_fn=lambda: logits,
#         false_fn=lambda: _top_k(),
#     )
#
#
# def top_p_logits(logits, p):
#     with tf.compat.v1.variable_scope('top_p_logits'):
#         logits_sort = tf.sort(logits, direction='DESCENDING')
#         probs_sort = tf.nn.softmax(logits_sort)
#         probs_sums = tf.cumsum(probs_sort, axis=1, exclusive=True)
#         logits_masked = tf.compat.v1.where(probs_sums < p, logits_sort, tf.ones_like(
#             logits_sort)*1000)  # [batchsize, vocab]
#         min_logits = tf.reduce_min(input_tensor=logits_masked, axis=1, keepdims=True)  # [batchsize, 1]
#         return tf.compat.v1.where(
#             logits < min_logits,
#             tf.ones_like(logits, dtype=logits.dtype) * -1e10,
#             logits,
#         )

def sample_sequence(*, hparams, length, start_token=None,
                    batch_size=None, context=None, temperature=1):
    if start_token is None:
        assert context is not None, 'Specify exactly one of start_token and context!'
    else:
        assert context is None, 'Specify exactly one of start_token and context!'
        context = tf.fill([batch_size, 1], start_token)

    def step(hparams, tokens, past=None):
        lm_output = model.model(hparams=hparams, X=tokens,
                                past=past, reuse=tf.compat.v1.AUTO_REUSE)

        logits = lm_output['logits'][:, :, :hparams.n_vocab]
        presents = lm_output['present']
        presents.set_shape(model.past_shape(
            hparams=hparams, batch_size=batch_size))
        return {
            'logits': logits,
            'presents': presents,
        }

    with tf.compat.v1.name_scope('sample_sequence'):
        start_time = time.time()
        context_output = step(hparams, context)
        print("total time 1: {}".format(time.time() - start_time))

        logits = context_output['logits'][:, -1, :] / tf.cast(temperature, tf.float32)

        return tf.nn.softmax(logits)[0]
