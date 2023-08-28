import pytz
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db.models import Q
from django.core.mail import send_mail
import secrets
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from uploader.models import Image

User = get_user_model()


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer



@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if Usuario.objects.filter(username=username).exists():
        return Response(
            {"message": "Usuário já existente!"}, status=status.HTTP_400_BAD_REQUEST
        )
    elif Usuario.objects.filter(email=email).exists():
        return Response(
            {"message": "Email já está sendo utilizado!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if username and email and password:
        user = User.objects.create(username=username)
        user.email = email
        user.set_password(password)
        user.save()

        response_data = {
            "message": "Usuário criado com sucesso!",
            "username": user.username,
            "email": user.email,
            "id": user.id,
            # Adicione outros campos do usuário que você deseja retornar
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Dados de usuário inválidos!"}, status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):
    value = request.data.get("value")
    password = request.data.get("password")
    print(value, password)

    if value is not None and password is not None:
        try:
            user = User.objects.get(Q(username=value) | Q(email=value))
            username = user.username
            user = authenticate(username=username, password=password)
        except User.DoesNotExist:
            user = None
            
    else:
        return Response(
            {"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST
        )

    print(user)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        response_data = {
            "refresh": str(refresh),
            "access": str(access),
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "message": "Login realizado com sucesso!"
            # Adicione outros campos do usuário que você deseja retornar
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST
        )


import smtplib
from email.mime.text import MIMEText


def enviar_email(destinatario, assunto, token, name):
    remetente = "trottingtomes@gmail.com"
    senha = "xektjmzuaveczuhh"

    with open('/home/faelbochi/Documentos/ifc/trabalhos/hackathon/back/usuario/email/token_change_password.html', 'r') as file:
        conteudo_html = file.read()

    conteudo_html = conteudo_html.replace('{name}', name)
    conteudo_html = conteudo_html.replace('{token}', token)

    # Criando a mensagem
    msg = MIMEMultipart()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    msg.attach(MIMEText(conteudo_html, 'html'))

    # Conectando ao servidor SMTP do Gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(remetente, senha)

    # Enviando o e-mail
    server.sendmail(remetente, destinatario, msg.as_string())
    server.quit()


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def forget_password(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": "Email não encontrado"}, status=status.HTTP_401_UNAUTHORIZED
        )
        pass
    else:
        if(user.password_reset_token is not None):
            user.password_reset_token = None
            
        # Gerar token exclusivo
        desired_length = 6
        token_size = (desired_length + 1) // 2 
        token = secrets.token_hex(token_size)[:desired_length]
        # Salvar o token, e-mail do usuário e data/hora
        user.password_reset_token = token
        user.password_reset_token_created = datetime.now(pytz.timezone('America/Sao_Paulo'))
        user.save()

        print(user.password_reset_token_created)
        # Enviar e-mail
        subject = "Redefinição de senha"
        to_email = email
        enviar_email(
            to_email,
            subject,
            token,
            name = user.username
        )

        response_data = {
            "id": user.id,
            "token": token,
            "message": "E-mail enviado com sucesso!",
        }
        # Exibir uma mensagem de sucesso na tela
        return Response(response_data, status=status.HTTP_200_OK)

TOKEN_EXPIRATION_SECONDS = 1200 

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def check_token_reset_password(request):
    id = request.data.get("user_id")
    token = request.data.get('token')

    try:
        user = User.objects.get(id=id)  # Alterar para 'id=usuario_id'
    except User.DoesNotExist:
        return Response(
            {"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    if user.password_reset_token_created:
        timezone = pytz.timezone('America/Sao_Paulo')
        current_time = datetime.now(timezone)
        expiration_time = current_time - user.password_reset_token_created
        
        print(expiration_time.total_seconds())
        if expiration_time.total_seconds() > TOKEN_EXPIRATION_SECONDS:
            user.password_reset_token = None
            user.password_reset_token_created = None
            user.save()
            return Response(
                {"message": "Token expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    if token == user.password_reset_token:
        return Response(
                {"message": "Token valido."},
                status=status.HTTP_200_OK,
            )

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def change_password(request):
    # Procurar usuário com base no token
    id = request.data.get("user_id")

    try:
        user = User.objects.get(id=id)  # Alterar para 'id=usuario_id'
    except User.DoesNotExist:
        return Response(
            {"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    if user.password_reset_token_created:
        timezone = pytz.timezone('America/Sao_Paulo')
        current_time = datetime.now(timezone)
        expiration_time = current_time - user.password_reset_token_created
        
        print(expiration_time.total_seconds())
        if expiration_time.total_seconds() > TOKEN_EXPIRATION_SECONDS:
            user.password_reset_token = None
            user.password_reset_token_created = None
            user.save()
            return Response(
                {"message": "Token expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
    # Atualizar a senha do usuário
    new_password = request.data.get("new_password")
    user.set_password(new_password)
    user.save()

    user.password_reset_token = ""
    user.password_reset_token_created = None
    user.save()

    return Response(
        {"message": "Senha atualizada com sucesso."}, status=status.HTTP_200_OK
    )

def upload_user_foto(user_id, image):
    user = User.objects.get(id=user_id)

    if user.foto is not None:
        existing_foto = Image.objects.get(attachment_key=user.foto.attachment_key)
        existing_foto.delete()

    # Agora, crie um novo registro de imagem para a foto enviada
    new_foto = Image.objects.create(file=image, description=f"Foto de perfil do usuário - {user.username}")
    user.foto = new_foto
    user.save()
    print(user.foto)


    response_data = {
        "foto": "Foto excluída com sucesso.",
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def edit_account(request):
    print(request.data.get("image"))
    print(request.data)
    user_id = request.data.get('user_id')
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    image = request.FILES.get("image")


    user = User.objects.get(id=user_id)

    if username != '' and username is not None and username != user.username:
        user.username = username

    if email != '' and email is not None and email != user.email:
        user.email = email

    if password != '' and password is not None and password != user.password:
        user.set_password(password)
        

    # upload_user_foto(user_id, image)
    user.save()

    response_data = {
        "message": "Usuário atualizado com sucesso.",
        "username": user.username,
        "email": user.email,
    }

    return Response(response_data, status=status.HTTP_200_OK)

