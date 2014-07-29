# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    objs_rows=db(db.objective.obj_owner==auth.user.id).select()
    objs_results_map={}
    if len(objs_rows) > 0:
        for objs_item in objs_rows:            
            key_result_rows=db(db.key_result.objective_id==objs_item.id).select()
            if len(key_result_rows) > 0:
                objs_results_map[objs_item.obj_content]=key_result_rows
    return dict(objs_rows=objs_rows,objs_results_map=objs_results_map)

@auth.requires_login()
def post_artifact():
    if len(request.args): key_result_id=int(request.args[0])
    else:
        return dict()
    form=SQLFORM(db.key_result_artifact,fields=['artifact'],labels={'artifact':'Add New artifact'})
    form.vars.key_result_id=key_result_id
    if form.process().accepted:
        response.flash='artifact accepted'
    elif form.errors:
        response.flash='errors'
    artifact_rows=db(db.key_result_artifact.key_result_id==key_result_id).select()
    return dict(artifact_rows=artifact_rows,form=form)
        

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
