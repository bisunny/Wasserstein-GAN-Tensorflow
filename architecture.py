import tensorflow as tf
import tensorflow.contrib.slim as slim
import sys

import config

sys.path.insert(0, 'ops/')

'''
   Leaky RELU
   https://arxiv.org/pdf/1502.01852.pdf
'''
def lrelu(x, leak=0.2, name='lrelu'):
   return tf.maximum(leak*x, x)

def netG(z, batch_size):

   print 'GENERATOR'
   z = slim.fully_connected(z, 4*4*1024, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='g_z')
   z = tf.reshape(z, [batch_size, 4, 4, 1024])
   print 'z:',z

   print 'z:',z
   conv1 = slim.convolution2d_transpose(z, 512, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='g_conv1')
   conv1 = tf.nn.relu(conv1)
   print 'conv1:',conv1

   conv2 = slim.convolution2d_transpose(conv1, 256, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='g_conv2')
   conv2 = tf.nn.relu(conv2)
   print 'conv2:',conv2

   conv3 = slim.convolution2d_transpose(conv2, 128, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='g_conv3')
   conv3 = tf.nn.relu(conv3)
   print 'conv3:',conv3

   conv4 = slim.convolution2d_transpose(conv3, 3, 5, stride=2, activation_fn=tf.identity, scope='g_conv4')
   conv4 = tf.nn.tanh(conv4)
   print 'conv4:',conv4
   print
   print 'END G'
   print

   tf.add_to_collection('vars', conv1)
   tf.add_to_collection('vars', conv2)
   tf.add_to_collection('vars', conv3)
   tf.add_to_collection('vars', conv4)

   return conv4 


'''
   Discriminator network
'''
def netD(input_images, batch_size, reuse=False):
   print 'DISCRIMINATOR' 
   sc = tf.get_variable_scope()
   with tf.variable_scope(sc, reuse=reuse):

      print 'input images:',input_images
      conv1 = slim.convolution(input_images, 64, 5, stride=2, activation_fn=tf.identity, scope='d_conv1')
      conv1 = lrelu(conv1)
      print 'conv1:',conv1

      conv2 = slim.convolution(conv1, 128, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='d_conv2')
      conv2 = lrelu(conv2)
      print 'conv2:',conv2
   
      conv3 = slim.convolution(conv2, 256, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='d_conv3')
      conv3 = lrelu(conv3)
      print 'conv3:',conv3

      conv4 = slim.convolution(conv3, 512, 5, stride=2, normalizer_fn=slim.batch_norm, activation_fn=tf.identity, scope='d_conv4')
      conv4 = lrelu(conv4)
      print 'conv4:',conv4

      conv5 = slim.convolution(conv4, 1, 4, stride=2, activation_fn=tf.identity, scope='d_conv5')
      print 'conv5:',conv5
      
      print 'END D\n'
      
      tf.add_to_collection('vars', conv1)
      tf.add_to_collection('vars', conv2)
      tf.add_to_collection('vars', conv3)
      tf.add_to_collection('vars', conv4)
      
      return conv4

