from data_preprocessing import *
from analysis import *
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding,Dot,Reshape,Dense,Multiply,Conv1D,GlobalAveragePooling1D,GlobalMaxPool1D,Dense,Concatenate,Flatten,Dropout
from tensorflow.keras import Model
from sklearn.model_selection import train_test_split
dict_size = 200
num_of_categorical = 2
ft_size = 32
def build_Neural_Net():
    """
    defining the NN for solving recommendation system
    it takes text data seperately from numeric, 
    uses the merge of those seperate columns infos to understand the general user-item behavior.
    it uses also 1dConv layers to pool info out of embeddings.
    the structure is very popular for movielens dataset.
    uses mse for loss function for optimization.
    """
    
    
    title_inp = Input(name = "title",shape =[None])

    user_id = Input(name = "userId",shape = [None])
    
    title_emb_left = Embedding(input_dim = 193609,output_dim = 100)(title_inp)
    user_emb_left = Embedding(input_dim = 610,output_dim = 100)(user_id)
    
    title_emb_right = Embedding(input_dim = 193609,output_dim = 100)(title_inp)
    user_emb_right = Embedding(input_dim = 610,output_dim = 100)(user_id)
    
    
    dot_concat = Multiply()([title_emb_left,user_emb_left])
    
    
    
    merge = Concatenate()([title_emb_right,user_emb_right])
    
    nxt_conv = Conv1D(filters = ft_size,kernel_size = 2,activation = 'relu',padding = 'same')(merge)
    nxt_conv = Conv1D(filters = ft_size,kernel_size = 2,activation = 'relu',padding = 'same')(nxt_conv)
    nxt_conv = Conv1D(filters = ft_size,kernel_size = 2,activation = 'relu',padding = 'same')(nxt_conv)
    
    
    all_concat = Concatenate()([dot_concat,nxt_conv])
    
    gl_maxpool = GlobalMaxPool1D()(all_concat)
    
    gl_averagepool = GlobalAveragePooling1D()(all_concat)
    
    flt_layer = Flatten()(all_concat)
    
    nxt_mrg = Concatenate()([gl_averagepool,gl_maxpool])
    
    
    
    last_layer = Dense(100,activation = 'relu')(nxt_mrg)
    last_layer = Dropout(0.2)(last_layer)
    last_layer = Dense(100,activation = 'relu')(last_layer)
    last_layer = Dropout(0.2)(last_layer)

    last_layer = Dense(1,activation = 'relu')(last_layer)

    
    model = Model([title_inp,user_id],last_layer)
    opt = tf.keras.optimizers.Adam(learning_rate=0.005)

    model.compile(optimizer = opt, loss='mse', metrics=['mean_absolute_error','mean_squared_error'])

    return model
def problem_solver():
    """
    reads the data in RecSystemFormat, defines the NN for the RecSystem,
    traines the model for 5 epochs, with evaluating on validation data which is 10% of all.
    returns the evaluation on test dataset.
    """
    
    data = rec_data()

    # read the data from the folder specified
    data.read_data('data/')

    data.data.rename(columns = {'movieId':'id'},inplace=True)
    
    
    data.data["genres"].apply(lambda x:x.split('|'))
    model = build_Neural_Net()
    train, test = train_test_split(data.data,random_state = 10)
    model.fit([train["id"],train["userId"]],train["rating"],validation_split=0.1,epochs = 1)
    print("Evaluation in Test " ,model.evaluate([test["id"],test["userId"]],test["rating"]))

problem_solver()