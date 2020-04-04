import tarfile
import os
import json
import requests
import sys
import shutil
import re
from tqdm import tqdm, trange
import numpy as np
import tensorflow as tf
from tensorflow.core.protobuf import rewriter_config_pb2
from tensorflow.python.client import device_lib
import time
from datetime import datetime
import csv
import argparse

import gpt_2_simple

from patches.sample import sample_sequence
gpt_2_simple.src.sample.sample_sequence = sample_sequence

from gpt_2_simple.src import model, sample, encoder, memory_saving_gradients
from gpt_2_simple.src.load_dataset import load_dataset, Sampler
from gpt_2_simple.src.accumulate import AccumulatingOptimizer

def generate(sess,
             text,
             run_name='run1',
             checkpoint_dir='checkpoint',
             model_name=None,
             model_dir='models',
             sample_dir='samples',
             return_as_list=False,
             sample_delim='=' * 20 + '\n',
             seed=None,
             nsamples=1,
             temperature=0.7,
             top_k=0,
             top_p=0.0,
             include_prefix=True):
    """Generates text from a model loaded into memory.
    Adapted from https://github.com/openai/gpt-2/blob/master/src/interactive_conditional_samples.py
    """

    if nsamples == 1:
        sample_delim = ''

    if model_name:
        checkpoint_path = os.path.join(model_dir, model_name)
    else:
        checkpoint_path = os.path.join(checkpoint_dir, run_name)

    enc = encoder.get_encoder(checkpoint_path)
    hparams = model.default_hparams()
    with open(os.path.join(checkpoint_path, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    context = tf.compat.v1.placeholder(tf.int32, [1, None])
    context_tokens = enc.encode(text)

    np.random.seed(seed)
    tf.compat.v1.set_random_seed(seed)

    start_time = time.time()

    proba_t = sample.sample_sequence(
        hparams=hparams,
        length=1,
        start_token=None,
        context=context,
        batch_size=1,
        temperature=temperature
    )

    print("total time A: {}".format(time.time() - start_time))
    start_time = time.time()

    proba = sess.run(proba_t, feed_dict={
            context: [context_tokens]
        })

    print("total time B: {}".format(time.time() - start_time))


    return proba
