from flask import Flask, render_template,redirect, request
import sqlite3
import os 
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# creamos una "base de datos" con 3 usuarios
baseDatos={
    1:{'id':'e1','nombre':'Felipe','apellido':'Castro','rol':1},
    2:{'id':'e2','nombre':'Camilo','apellido':'osorio','rol':1},
    3:{'id':'a3','nombre':'Pepe','apellido':'cardona','rol':2},
    4:{'id':'s4','nombre':'Maria','apellido':'perez','rol':3}
}


retroalimentacionEmpleados ={}
#VARIABLES
tipo_user = ''
id_user = ''
nombre = ''
valorId = 5

#1:empleado
#2:administrador
#3:Superadminstrador

@app.route('/',methods = ["GET","POST"])
def login():
    return render_template("Login.html")

@app.route('/ingreso', methods = ["POST"]) #aca se valida el usuario
def ingreso():
    global tipo_user,id_user, nombre
    
    if request.method=="GET":
         return render_template("Login.html")
    else:
        #vamos a la base de datos y valido y redirecciono a la pagina de administracion

        formUser=request.form['user']
        formContraseña=request.form['contraseña']
        try:
            with sqlite3.connect("D:\Downloads\GestionEmpleados\SGE") as con:
                cur= con.cursor()
                registro = cur.execute("select * from datos where usuario = ?",[formUser]).fetchone()
               
                if registro !=None:
                    #if check_password_hash(registro[2],formContraseña):#desencripto y calido contraseña
                        # registro2=cur.execute("select id,nombre,rol from empleado where id = ?"[registro[0]])
                        # nombre=registro2[1]
                        # tipo_user=registro2[2]
                        # id_user=registro2[0]
                        return redirect('/administrador')   
        except:
            con.rollback()
    
    return redirect('/')
   

@app.route('/administrador/<int:id_usuario>/',methods = ["GET"])
@app.route('/administrador',methods = ["GET"])
def administrador ():
    return render_template('administrador.html',
    tipo_user=tipo_user,
    id_user=id_user,
    nombre=nombre
    )


@app.route('/salir', methods = ["POST"])
def salir():
    global tipo_user
    tipo_user=0

    return redirect('/')


@app.route('/e_retroalimentación/<id_usuario>', methods = ["GET"])
def e_retroalimentación (id_usuario):
    if bool(retroalimentacionEmpleados):
        retro = retroalimentacionEmpleados[id_usuario]
    else:
        retro = ''
    return render_template('base-Retroalimentacion.html',
    tipo_user=tipo_user,
    id_user=id_usuario,
    nombre=nombre,
    retro = retro
    )


@app.route('/e_informacionpersonal/<id_usuario>', methods = ["GET"])
def e_informacionpersonal(id_usuario):
    return render_template('base-info.html',
    tipo_user=tipo_user,
    id_user=id_usuario,
    nombre=nombre,
    baseDatos=baseDatos)

@app.route('/crear_empleado', methods = ["POST"])
def crear_empleado ():
    #recuperar la info del formulario de crear empleado, y procesarla(mandarla a la base de datos)
    #retornar a la ventana de inicio 
    nombreU = request.form['crear-nombre']
    apellido= request.form['crear-apellido']
    cedula= request.form['crear-cedula']
    usuario= request.form['crear-usuario']
    contrasena= request.form['crear-contraseña'] 
    fechaIngreso= request.form['crear-fecha-ingreso']
    FechaTerminacion= request.form['crear-fecha-ingreso']
    Rol= request.form['tipo-rol']
    Salario= request.form['crear-salario']
    dependencia= request.form['crear-dependencia']
    global valorId 
    global baseDatos
    if Rol == 'empleado':
        Rol = 1
        subId = 'e'+ str(valorId)
    elif Rol == 'administrador':
        Rol= 2
        subId = 'a'+ str(valorId)
    else:
        Rol = 3   
        subId = 's'+ str(valorId)
    baseDatos [valorId] = {'id':subId,'nombre':nombreU,'apellido':apellido,'rol':Rol}
    valorId +=1
    return redirect('/administrador')

@app.route('/lista-empleados',methods=["GET"])
def listarEmpleados():
    Lista = {}
    if tipo_user == 2:
        for Actusuario in baseDatos:
            if nombre != baseDatos.get(Actusuario).get('nombre') and baseDatos.get(Actusuario).get('rol') != 3:
                Lista[Actusuario] = baseDatos.get(Actusuario)
    else:
        for Actusuario in baseDatos:
            if nombre != baseDatos.get(Actusuario).get('nombre'):
                Lista[Actusuario] = baseDatos.get(Actusuario)
            
    return render_template('base-lista-empleados.html',
    tipo_user=tipo_user,
    id_user=id_user,
    baseDatos=Lista,
    nombre=nombre
    )

@app.route('/buscar_empleado', methods = ["POST"])
def buscar_empleado ():
    buscar=request.form['buscar']
    try:
        base=baseDatos[int(buscar)]
    except:
        pass
    
    return render_template('base-ResultadosBusqueda.html',
    tipo_user=tipo_user,
    id_user=id_user,
    baseDatos=base,
    nombre=nombre
    )

@app.route('/eliminar_empleado/<int:id_usuario>', methods = ["GET", "POST"])
def eliminar_empleado (id_usuario):
    #recibir el id del empleado donde se presiono eliminar para bucarlo en la base y eliminarlo 
    baseDatos.pop(id_usuario)
    return redirect('/lista-empleados')


@app.route('/generar_retroalimentación/<int:id_usuario>', methods = ["POST"])
def generar_retroalimentación (id_usuario):
    if request.method == 'POST':
        global retroalimentacionEmpleados
        fecha = request.form['Fecha']
        retroalimentacion = request.form['retroalimentacion-text']
        puntaje = request.form['puntaje']
        retroalimentacionEmpleados[baseDatos[id_usuario].get('id')] ={'Fecha':fecha,'Retroalimentacion':retroalimentacion,'Puntaje':puntaje}
        return redirect('/lista-empleados')


@app.route('/editar_empleado/<int:id_usuario>', methods = ["POST"])
def editar_empleado (id_usuario):
    if request.method == 'POST':
      nombre = request.form['crear-nombre']      
      apellido = request.form['crear-apellido']
      baseDatos[id_usuario]['nombre'] = nombre
      baseDatos[id_usuario]['apellido'] = apellido
      return redirect('/lista-empleados')
#HASTA ACA ORGANIZADO////////////////////////////////////////////////////////////////////////////// 





#recibir el id 

# @app.route('/superadministrador', methods = ["GET"])
# def superadministrador ():
#     return "Estás en superadministrador"

# @app.route('/asignar_roles', methods = ["GET", "POST"])
# def asignar_roles ():
#     return "Estás en la página para asignar roles"


if __name__ == "__main__":
    app.run(debug=True)