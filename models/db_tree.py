# coding: utf8
db.define_table('objective',Field('obj_content',required=True),Field('obj_owner','reference auth_user'),auth.signature)
db.objective.obj_content.requires=IS_NOT_EMPTY()
db.objective.obj_owner.requires=IS_IN_DB(db,db.auth_user.id,"%(last_name)s %(first_name)s")

db.define_table('key_result',Field('result_content',required=True),Field('objective_id','reference objective'),auth.signature)
db.key_result.objective_id.requires=IS_IN_DB(db,db.objective.id,'%(obj_content)s')
db.key_result.result_content.requires=IS_NOT_EMPTY()

db.define_table('key_result_artifact',Field('artifact'),Field('key_result_id','reference key_result'),auth.signature)
db.key_result_artifact.artifact.requires=IS_NOT_EMPTY()
db.key_result_artifact.key_result_id.requires=IS_IN_DB(db,db.key_result.id,'%(result_content)s')
