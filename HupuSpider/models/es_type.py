from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerDoc, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections

   
connections.create_connection(hosts=["localhost"])


class HupuType(DocType):

    teamname = Text(analyzer="ik_max_word")
    teamurl = Keyword()
    newstitle = Text(analyzer="ik_max_word")
    newsurl = Keyword()
    content = Text(analyzer="ik_max_word")
    imageurl = Keyword()

    # class Meta:
    #     index = 'hupu'
    #     doc_type= 'doc'

    class Index:
        name = 'hupu'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
    	return super(HupuType, self).save(** kwargs)
   

if __name__ == "__main__":

    HupuType.init()
