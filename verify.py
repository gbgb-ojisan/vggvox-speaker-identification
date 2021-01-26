#!/bin/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine

from utils import logger
from model import vggvox_model
from wav_reader import get_fft_spectrum
import constants as c

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def build_buckets(max_sec, step_sec, frame_step):
	buckets = {}
	frames_per_sec = int(1/frame_step)
	end_frame = int(max_sec*frames_per_sec)
	step_frame = int(step_sec*frames_per_sec)
	for i in range(0, end_frame+1, step_frame):
		s = i
		s = np.floor((s-7+2)/2) + 1  # conv1
		s = np.floor((s-3)/2) + 1  # mpool1
		s = np.floor((s-5+2)/2) + 1  # conv2
		s = np.floor((s-3)/2) + 1  # mpool2
		s = np.floor((s-3+2)/1) + 1  # conv3
		s = np.floor((s-3+2)/1) + 1  # conv4
		s = np.floor((s-3+2)/1) + 1  # conv5
		s = np.floor((s-3)/2) + 1  # mpool5
		s = np.floor((s-1)/1) + 1  # fc6
		if s > 0:
			buckets[i] = int(s)

	return buckets

def get_embedding(model, wav_file, max_sec):
 	buckets = build_buckets(max_sec, c.BUCKET_STEP, c.FRAME_STEP)
 	signal = get_fft_spectrum(wav_file, buckets)
 	embedding = np.squeeze(model.predict(signal.reshape(1,*signal.shape,1)))
 	return embedding

def main(args):
    logger.info("Loading model weights from [{}]....".format(c.WEIGHTS_FILE))
    model = vggvox_model()
    model.load_weights(c.WEIGHTS_FILE)
    # model.summary()

    logger.info("Processing target sample....")
    embedding_t = get_embedding(model, args.target, c.MAX_SEC)

    logger.info("Processing query sample....")
    embedding_q = get_embedding(model, args.query, c.MAX_SEC)

    score = cosine_similarity(embedding_q, embedding_t)

    logger.info('Target: {}, Query: {}, Score: {}'.format(args.target, args.query, score))

    return score

if __name__ == '__main__':
    # Building argument parser
    parser = argparse.ArgumentParser(description='Script for Voice Verification (1:1 matching) based on VGGVOX.')
    parser.add_argument('target', type=str, help='Target voice')
    parser.add_argument('query', type=str, help='Query voice')
    args = parser.parse_args()

    # Building logger
    logger = logger.setup_logger('.', 'DEBUG')

    main(args)
