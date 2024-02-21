from flask import Blueprint
from models import Company ,db
from flask import jsonify, request

company_bp=Blueprint("company",__name__)

@company_bp.route('/companies', methods=['POST'])
def create_company():
    data=request.json
    new_company=Company(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        description=data['description'],
        category=data['category']
        
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company created successfully'}), 201

@company_bp.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    result = [{'id': company.id, 'name': company.name} for company in companies]
    return jsonify({'companies': result}), 200

@company_bp.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get(company_id)
    if company:
        return jsonify({'id': company.id, 'name': company.name, 'email': company.email}), 200
    else:
        return jsonify({'message': 'Company not found'}), 404
    

@company_bp.route('/companies/<int:company_id>', methods=['PATCH'])
def update_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    data = request.json
    company.name = data.get('name', company.name)
    company.email = data.get('email', company.email)
    company.password = data.get('password', company.password)
    company.description = data.get('description', company.description)
    company.category = data.get('category', company.category)
    db.session.commit()
    return jsonify({'message': 'Company updated successfully'}), 200

@company_bp.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': 'Company deleted successfully'}), 200



    
    
