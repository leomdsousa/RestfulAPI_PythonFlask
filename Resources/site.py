from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import (create_access_token
                                , jwt_required
                                , get_raw_jwt)
from Resources.filters import normalizeSitePathParams, consulta_site_com_url, consulta_site_sem_url
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('url', type=str)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Sites(Resource):
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    def get(self):
        params = path_params.parse_args()
        params_valids = { valor:params[valor] for valor in params if params[valor] is not None } 
        parameters = normalizeSitePathParams(**params_valids)

        if parameters.get('url'):
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta_site_com_url, tupla)
        else:
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta_site_sem_url, tupla)

        sites = []
        for linha in result:
            sites.append({
                'id': linha[0]
                , 'url': linha[1]
            })

        return { 'hoteis': sites }

class Site(Resource):

    argumento = reqparse.RequestParser()
    argumento.add_argument('url', type=str, required=True, help='The field nome must be filled')

    def get(self, url):
        site = SiteModel.find_by_url(url)
        
        if site:
            return site.convertToDictionary()
        return {'Message': 'Site not found'}, 404

    @jwt_required
    def post(self, url):
        site = SiteModel.find_by_url(url)
        if site:
            return {'Message': 'Hotel already exists'}, 400

        dados = Site.argumento.parse_args()
        site = SiteModel(**dados)
        
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'Message': "There's no hotel linked to the site delivered"}, 400

        try:
            site.save_site()
            return site.convertToDictionary(), 201
        except:
            return {'Message': 'An internal error ocurred while attempting to save the data'}, 500
        
    @jwt_required
    def delete(self, url):
        site = SiteModel.find_by_url(url)
        
        if site:
            try:
                site.delete_site()
                return { 'hoteis': [site.convertToDictionary() for site in SiteModel.find_all() ] }
            except:
                return {'Message': 'An internal error ocurred while attempting to save the data'}, 500                

        return {'Message': 'Hotel not found'}, 404        

