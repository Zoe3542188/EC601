from skimage import io,transform
import tensorflow as tf
import numpy as np
import Image


path1 = "E:/data/datasets/flower_photos/daisy/5547758_eea9edfd54_n.jpg"
#path to your test image
#path2 = "E:/data/datasets/flower_photos/daisy/5547758_eea9edfd54_n.jpg"
#path3 = "E:/data/datasets/flower_photos/daisy/5547758_eea9edfd54_n.jpg"

flower_dict = {0:'roses',1:'sunflowers'}

w=100
h=100
c=3

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    #data2 = read_one_image(path2)
    #data3 = read_one_image(path3)
    #data4 = read_one_image(path4)
    #data5 = read_one_image(path5)
    data.append(data1)
    #data.append(data2)
    #data.append(data3)
    #data.append(data4)
    #data.append(data5)
    #the path to your trained model
    saver = tf.train.import_meta_graph('data/model.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint('data/'))
    #save your check point
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)

    #print the predicted matrix
    print(classification_result)
    #print max value in rows
    print(tf.argmax(classification_result,1).eval())
    #get flower name in dict
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        print("The sample u input is "+flower_dict[output[i]])
        img = Image.open(path1)
        img.show