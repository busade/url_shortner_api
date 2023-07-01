from flask_restx import Namespace, Resource, fields
from flask import request,redirect
from ..models.urls import Links, Analysis
from ..models.users import Users
from urllib.parse import urlparse
import httplib2, random,string,qrcode
import geocoder, requests
from http import HTTPStatus 
from io import BytesIO
from flask_jwt_extended import jwt_required,get_jwt_identity


links_namespace = Namespace('links', description='Links related operations')

link_model= links_namespace.model("Links",{
                    'id': fields.Integer(description="id"),
                    'long_url':fields.String(required=True,description="long url"),
                    'link': fields.String(description="short url"),
                    'qr_code': fields.String(description="qrcode"),
                    'user_id': fields.Integer(description="user id"),
                    'custom_url': fields.String(description="custom url prefix"),
                    'created_at': fields.DateTime(description="created at")

})
analysis_model= links_namespace.model("Analysis",{
                    'id': fields.Integer(description="id"),
                    'link_id': fields.Integer(description="link id"),
                    'ip_address': fields.String(description="ip address"),
                    'country': fields.String(description="country"),
                    'city': fields.String(description="city"),
                    'visit_count': fields.Integer(description="visit count")
})

def generate_qrcode(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='orange', back_color='white')
    qr_code = img.save('slit.png')    
    return img
def generate_short_url():
    base = "slit.ly/"
    char = string.ascii_letters + string.digits
    res = ''.join(random.choices(char, k=6))
    ur= base +res
    return ur
def custom(custom_url):
    res = custom_url
    return res + ".com"
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_working(url):
    http = httplib2.Http()
    try:
        response, _ = http.request(url, "HEAD")
        return response.status == 200 and response.status < 400
    except:
        return False
    
    
@links_namespace.route('/')

class short_url(Resource):
    
    @links_namespace.expect(link_model)
    @links_namespace.marshal_with(link_model)
    @jwt_required()
    def post(self):
        '''Shorten URL'''
        data= request.get_json()
        url=data['long_url']
        qrcode = generate_qrcode(url)
        buffer = BytesIO()
        qrcode.save(buffer)
        qrcode = buffer.getvalue()
        user= Users.query.filter_by(id=get_jwt_identity()).first()
        check = Links.query.filter_by(long_url=url).first()

        if check:
            return check.link
        else:
            if is_valid_url(url)  and is_working(url):
                    new_url = Links(
                        long_url=url,
                        link = generate_short_url(),
                        qr_code=qrcode,
                        user_id=user.id
                    )
                    new_url.save()
                    return new_url,HTTPStatus.CREATED
            else:
                return {'message': "link invalid"}, HTTPStatus.FORBIDDEN




@links_namespace.route('/short_url/<int:url_id>')
class  Details(Resource):
    @links_namespace.marshal_with(link_model) 
    @links_namespace.doc(
        description="Redirect to long url",
        params={'url_id': 'A short url'}
    )
    @jwt_required()  
    def get(self,url_id):
        '''Take record of where a user is browsing from'''
        short_url = Links.query.filter_by(id=url_id).first()
        response = requests.get('https://ipapi.co/json/').json()
        
        city= response["city"]
        country= response["country_name"]
        ip= response["ip"]
        visits= Links.query.filter_by(link=url_id)
        count = 0
        if visits:
            new_analysis = Analysis(
                link_id = url_id,
                ip_address = ip,
                country = country,
                city = city,
                visit_count = count+1
        )
        new_analysis.save()
    
        return short_url,HTTPStatus.OK

    

@links_namespace.route('/short_urls')
class RetrieveUrls(Resource):
    @links_namespace.marshal_with(link_model)
    @links_namespace.doc(description="Get all urls",)
    @jwt_required()
    def get(self):
        """Get all urls by user id"""
        user = Users.query.filter_by(id=get_jwt_identity()).first()
        urls = user.link
        return urls,HTTPStatus.OK


@links_namespace.route('/custom')
class CustomLinks(Resource):
    @links_namespace.expect(link_model)
    @links_namespace.marshal_with(link_model)
    @links_namespace.doc(description="Create custom Links")
    @jwt_required()
    def post(self):
        """Create custom Links"""
        data = request.get_json()
        url = data['long_url']
    
        qrcode = generate_qrcode(url)
        buffer = BytesIO()
        qrcode.save(buffer)
        qrcode = buffer.getvalue()
        user= Users.query.filter_by(id=get_jwt_identity()).first()
        custom_url=data['custom_url']
        c= custom(custom_url)
        check = Links.query.filter_by(long_url=url).first()
        if check:
            return check.custom_url
        else:
            if is_valid_url(url)  and is_working(url):
                    new_url = Links(
                        long_url=url,
                        link= c,
                        qr_code=qrcode,
                        user_id=user.id,
                        custom_url=c
                    )
                    new_url.save()
                    return new_url,HTTPStatus.CREATED
            else:
                return {'message': "link  is invalid"}, HTTPStatus.FORBIDDEN
            
@links_namespace.route('/custom/<int:custom_id>')
class RetriveCustom(Resource):
    @links_namespace.marshal_with(link_model)
    @links_namespace.doc(description="Retrieve a custom url by id",
                         params={'custom_id': 'A custom url id'})
    @jwt_required()
    def get(self,custom_id):
        """Retrieve a custom url by id"""
        c= Links.query.filter_by(id=custom_id).first()
        return c, HTTPStatus.OK
    
@links_namespace.route('/custom/all')
class GetAll(Resource):
    @links_namespace.marshal_with(link_model)
    @links_namespace.doc(description="Retrive all custom url")
    @jwt_required()
    def get(self):
        """Retrive all custom url"""
        User = Users.query.filter_by(id=get_jwt_identity()).first()
        c= User.link
        return c, HTTPStatus.OK

