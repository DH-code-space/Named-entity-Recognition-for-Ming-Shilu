from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TransformerWordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

# define columns
columns = {0: 'text', 1: 'ner'}

# this is the folder in which train, test and dev files reside
data_folder = './'

# init a corpus using column format, data folder and the names of the train, dev and test files
corpus: Corpus = ColumnCorpus(data_folder, columns, train_file='train.txt', test_file='test.txt', dev_file='dev.txt')

print(corpus)

label_type = 'ner'

label_dict = corpus.make_label_dictionary(label_type=label_type)

embeddings = TransformerWordEmbeddings(model="Jihuai/bert-ancient-chinese", fine_tune=True, use_context=True, model_max_length=512)

tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type=label_type, use_crf=True)

trainer = ModelTrainer(tagger, corpus)

trainer.train('resources/taggers/sota-ner-flair', learning_rate=0.01, mini_batch_size=8, max_epochs=100)
