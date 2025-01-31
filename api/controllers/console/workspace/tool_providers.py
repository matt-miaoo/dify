import json

from libs.login import login_required
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask import send_file
from werkzeug.exceptions import Forbidden

from controllers.console import api
from controllers.console.setup import setup_required
from controllers.console.wraps import account_initialization_required

from services.tools_manage_service import ToolManageService

import io

class ToolProviderListApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        return ToolManageService.list_tool_providers(user_id, tenant_id)

class ToolBuiltinProviderListToolsApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self, provider):
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        return ToolManageService.list_builtin_tool_provider_tools(
            user_id,
            tenant_id,
            provider,
        )

class ToolBuiltinProviderDeleteApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self, provider):
        if not current_user.is_admin_or_owner:
            raise Forbidden()
        
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        return ToolManageService.delete_builtin_tool_provider(
            user_id,
            tenant_id,
            provider,
        )
    
class ToolBuiltinProviderUpdateApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self, provider):
        if not current_user.is_admin_or_owner:
            raise Forbidden()
        
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()
        parser.add_argument('credentials', type=dict, required=True, nullable=False, location='json')

        args = parser.parse_args()

        return ToolManageService.update_builtin_tool_provider(
            user_id,
            tenant_id,
            provider,
            args['credentials'],
        )

class ToolBuiltinProviderIconApi(Resource):
    @setup_required
    def get(self, provider):
        icon_bytes, minetype = ToolManageService.get_builtin_tool_provider_icon(provider)
        return send_file(io.BytesIO(icon_bytes), mimetype=minetype)


class ToolApiProviderAddApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        if not current_user.is_admin_or_owner:
            raise Forbidden()
        
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()
        parser.add_argument('credentials', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('schema_type', type=str, required=True, nullable=False, location='json')
        parser.add_argument('schema', type=str, required=True, nullable=False, location='json')
        parser.add_argument('provider', type=str, required=True, nullable=False, location='json')
        parser.add_argument('icon', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('privacy_policy', type=str, required=False, nullable=True, location='json')

        args = parser.parse_args()

        return ToolManageService.create_api_tool_provider(
            user_id,
            tenant_id,
            args['provider'],
            args['icon'],
            args['credentials'],
            args['schema_type'],
            args['schema'],
            args.get('privacy_policy', ''),
        )

class ToolApiProviderGetRemoteSchemaApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('url', type=str, required=True, nullable=False, location='args')

        args = parser.parse_args()

        return ToolManageService.get_api_tool_provider_remote_schema(
            current_user.id,
            current_user.current_tenant_id,
            args['url'],
        )
    
class ToolApiProviderListToolsApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()

        parser.add_argument('provider', type=str, required=True, nullable=False, location='args')

        args = parser.parse_args()

        return ToolManageService.list_api_tool_provider_tools(
            user_id,
            tenant_id,
            args['provider'],
        )

class ToolApiProviderUpdateApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        if not current_user.is_admin_or_owner:
            raise Forbidden()
        
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()
        parser.add_argument('credentials', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('schema_type', type=str, required=True, nullable=False, location='json')
        parser.add_argument('schema', type=str, required=True, nullable=False, location='json')
        parser.add_argument('provider', type=str, required=True, nullable=False, location='json')
        parser.add_argument('original_provider', type=str, required=True, nullable=False, location='json')
        parser.add_argument('icon', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('privacy_policy', type=str, required=True, nullable=True, location='json')

        args = parser.parse_args()

        return ToolManageService.update_api_tool_provider(
            user_id,
            tenant_id,
            args['provider'],
            args['original_provider'],
            args['icon'],
            args['credentials'],
            args['schema_type'],
            args['schema'],
            args['privacy_policy'],
        )

class ToolApiProviderDeleteApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        if not current_user.is_admin_or_owner:
            raise Forbidden()
        
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()

        parser.add_argument('provider', type=str, required=True, nullable=False, location='json')

        args = parser.parse_args()

        return ToolManageService.delete_api_tool_provider(
            user_id,
            tenant_id,
            args['provider'],
        )

class ToolApiProviderGetApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        user_id = current_user.id
        tenant_id = current_user.current_tenant_id

        parser = reqparse.RequestParser()

        parser.add_argument('provider', type=str, required=True, nullable=False, location='args')

        args = parser.parse_args()

        return ToolManageService.get_api_tool_provider(
            user_id,
            tenant_id,
            args['provider'],
        )

class ToolBuiltinProviderCredentialsSchemaApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self, provider):
        return ToolManageService.list_builtin_provider_credentials_schema(provider)

class ToolApiProviderSchemaApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('schema', type=str, required=True, nullable=False, location='json')

        args = parser.parse_args()

        return ToolManageService.parser_api_schema(
            schema=args['schema'],
        )

class ToolApiProviderPreviousTestApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('tool_name', type=str, required=True, nullable=False, location='json')
        parser.add_argument('credentials', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('parameters', type=dict, required=True, nullable=False, location='json')
        parser.add_argument('schema_type', type=str, required=True, nullable=False, location='json')
        parser.add_argument('schema', type=str, required=True, nullable=False, location='json')

        args = parser.parse_args()

        return ToolManageService.test_api_tool_preview(
            current_user.current_tenant_id,
            args['tool_name'],
            args['credentials'],
            args['parameters'],
            args['schema_type'],
            args['schema'],
        )

api.add_resource(ToolProviderListApi, '/workspaces/current/tool-providers')
api.add_resource(ToolBuiltinProviderListToolsApi, '/workspaces/current/tool-provider/builtin/<provider>/tools')
api.add_resource(ToolBuiltinProviderDeleteApi, '/workspaces/current/tool-provider/builtin/<provider>/delete')
api.add_resource(ToolBuiltinProviderUpdateApi, '/workspaces/current/tool-provider/builtin/<provider>/update')
api.add_resource(ToolBuiltinProviderCredentialsSchemaApi, '/workspaces/current/tool-provider/builtin/<provider>/credentials_schema')
api.add_resource(ToolBuiltinProviderIconApi, '/workspaces/current/tool-provider/builtin/<provider>/icon')
api.add_resource(ToolApiProviderAddApi, '/workspaces/current/tool-provider/api/add')
api.add_resource(ToolApiProviderGetRemoteSchemaApi, '/workspaces/current/tool-provider/api/remote')
api.add_resource(ToolApiProviderListToolsApi, '/workspaces/current/tool-provider/api/tools')
api.add_resource(ToolApiProviderUpdateApi, '/workspaces/current/tool-provider/api/update') 
api.add_resource(ToolApiProviderDeleteApi, '/workspaces/current/tool-provider/api/delete')
api.add_resource(ToolApiProviderGetApi, '/workspaces/current/tool-provider/api/get')
api.add_resource(ToolApiProviderSchemaApi, '/workspaces/current/tool-provider/api/schema')
api.add_resource(ToolApiProviderPreviousTestApi, '/workspaces/current/tool-provider/api/test/pre')
