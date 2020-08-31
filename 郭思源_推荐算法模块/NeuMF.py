"""
Created on Aug 26, 2020
Tensorflow Implementation of Neural Matrix Factorization (NeuMF) recommender model in:
He Xiangnan et al. Neural Collaborative Filtering. In WWW 2017.
@author: Siyuan Guo (21171617, guosy2117@gmail.com)
"""
import tensorflow as tf


class NeuMF():
    def __init__(self, user_num, item_num, d, l2_reg_lambda):
        self.user_id = tf.placeholder(dtype=tf.int32, shape=[None])
        self.item_id = tf.placeholder(dtype=tf.int32, shape=[None])
        self.y = tf.placeholder(dtype=tf.float32, shape=[None])
        self.P = tf.placeholder(dtype=tf.float32, shape=[None])

        self.pg = tf.Variable(tf.random_normal([user_num, d], stddev=0.1))
        self.qg = tf.Variable(tf.random_normal([item_num, d], stddev=0.1))
        self.pm = tf.Variable(tf.random_normal([user_num, d], stddev=0.1))
        self.qm = tf.Variable(tf.random_normal([user_num, d], stddev=0.1))

        # GMF
        pu_g = tf.nn.embedding_lookup(self.pg, self.user_id)
        qi_g = tf.nn.embedding_lookup(self.qg, self.item_id)
        z_g = tf.multiply(pu_g, qi_g)

        # MLP
        pu_m = tf.nn.embedding_lookup(self.pm, self.user_id)
        qi_m = tf.nn.embedding_lookup(self.qm, self.item_id)
        x_m = tf.concat([pu_m, qi_m], 1)

        W1 = tf.Variable(tf.random_normal([2*d, 4*d], stddev=0.1))
        b1 = tf.Variable(tf.constant(0., shape=[4*d]))
        z1 = tf.nn.relu(tf.matmul(x_m, W1) + b1)

        W2 = tf.Variable(tf.zeros([4*d, 2*d]))
        b2 = tf.Variable(tf.constant(0., shape=[2*d]))
        z2 = tf.nn.relu(tf.matmul(z1, W2) + b2)

        W3 = tf.Variable(tf.zeros([2*d, d]))
        b3 = tf.Variable(tf.constant(0., shape=[d]))
        z3 = tf.nn.relu(tf.matmul(z2, W3) + b3)

        # NeuMF
        h = tf.Variable(tf.random_normal([2*d, 1], stddev=0.1))
        x = tf.concat([z_g, z3], 1)
        self.prediction = tf.nn.relu(tf.matmul(x, h))
        self.prediction = tf.reshape(self.prediction, [-1])

        self.loss = tf.reduce_sum(tf.div(tf.square(self.prediction - self.y), self.P))  # mse
        l2_loss = tf.nn.l2_loss(self.pg) + tf.nn.l2_loss(self.qg) + tf.nn.l2_loss(self.pm) + tf.nn.l2_loss(self.qm) + \
            tf.nn.l2_loss(W1) + tf.nn.l2_loss(W2) + tf.nn.l2_loss(W3)
        self.losses = self.loss + l2_reg_lambda * l2_loss
        self.mae = tf.reduce_sum(tf.abs(self.y - self.prediction))
        self.mse = tf.reduce_sum(tf.square(self.y - self.prediction))
