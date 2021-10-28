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
Roles={
    "empleado":3,
    "administrador":2,
    "superadministrador":1
}

retroalimentacionEmpleados ={}
#VARIABLES
tipo_user = ''
id_user = ''
nombre = ''
valorId = 6
session=False #verifica si esta loguiado
#1:empleado
#2:administrador
#3:Superadminstrador

@app.route('/',methods = ["GET","POST"])
def login():
    return render_template("Login.html")

@app.route('/ingreso', methods = ["POST"]) #aca se valida el usuario
def ingreso():
    global tipo_user,id_user, nombre, session
    
    if request.method=="GET":
         return render_template("Login.html")
    else:
        #vamos a la base de datos y valido y redirecciono a la pagina de administracion

        formUser=request.form['user']
        formContraseña=request.form['contraseña']
        try:
            with sqlite3.connect("SGE") as con:
                cur= con.cursor()
                registro = cur.execute("select * from datos where usuario = ?",[formUser]).fetchone()
                print("norml")
                print(registro)
                if registro !=None:
                    if check_password_hash(registro[2],formContraseña):#desencripto y calido contraseña
                        print("valida")
                        session=True
                        #registro2=cur.execute("select * from empleado where id = ?"[registro[0]])
                        #nombre=registro2[1]
                        #tipo_user=registro2[2]
                        #id_user=registro2[0]
                        return redirect('/administrador')   
        except:
            con.rollback()
    
    return redirect('/')
   

@app.route('/administrador/<int:id_usuario>/',methods = ["GET"])
@app.route('/administrador',methods = ["GET"])
def administrador ():
    global session
    print()
    if session:
        return render_template('administrador.html',
        tipo_user=tipo_user,
        id_user=id_user,
        nombre=nombre
        )
    else:
        return redirect("/")


@app.route('/salir', methods = ["POST"])
def salir():
    global tipo_user
    tipo_user=0

    return redirect('/')


@app.route('/e_retroalimentación/<id_usuario>', methods = ["GET"])
def e_retroalimentación (id_usuario):
    try:
        with sqlite3.connect("SGE") as con:
            cur= con.cursor()
            data = cur.execute("SELECT * FROM retroalimentacion where id_empleado=?;",[id_usuario])#sentencia  
            print(data)
            con.commit()
            return redirect('/lista-empleados')
              
    except:
            con.rollback()
    
    return render_template('base-Retroalimentacion.html',
    tipo_user=tipo_user,
    id_user=id_usuario,
    nombre=nombre,
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
    contra_cifrada=generate_password_hash(contrasena) #esta es la contraseña que hay que guardar en la base de datos
   
    tipocontrato=request.form['tipo-contrato']
    fechaIngreso= request.form['crear-fecha-ingreso']
    FechaTerminacion= request.form['crear-fecha-ingreso']
    Rol= request.form['tipo-rol']
    tipoContrato = request.form['tipo-contrato']
    Salario= request.form['crear-salario']
    dependencia= request.form['crear-dependencia']
    # global valorId 
    # global baseDatos
    # if Rol == 'empleado':
    #     Rol = 1
    #     subId = 'e'+ str(valorId)
    # elif Rol == 'administrador':
    #     Rol= 2
    #     subId = 'a'+ str(valorId)
    # else:
    #     Rol = 3   
    #     subId = 's'+ str(valorId)
    # baseDatos [valorId] = {'id':subId,'nombre':nombreU,'apellido':apellido,'rol':Rol}
    # valorId +=1
    try:
            with sqlite3.connect("SGE") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO datos (id,usuario,contrasena) VALUES (?,?,?)",(cedula,usuario,contra_cifrada)).fetchone()
                cur.execute("INSERT INTO empleado (cedula,nombre,apellido,cargo,salario,rol_id,fechatermino,fechainicio,tipocontrato,dependencia) VALUES (?,?,?,?,?,?,?,?,?,?)",(cedula,nombreU,apellido,Rol,Salario,Roles[Rol],FechaTerminacion,fechaIngreso,tipoContrato,dependencia)).fetchone()
                con.commit()
    except Exception:
        print(Exception.args[0])
        con.rollback()
    return redirect('/administrador')

@app.route('/lista-empleados',methods=["GET"])
def listarEmpleados():
    baseDatos2={}
    try:

        with sqlite3.connect("SGE") as con:
                    #con.row_factory=sqlite3.Row
                    cur= con.cursor()
                    cur.execute("select * from empleado")
                    lista=cur.fetchall()
                    print(len(lista))
                    j=0
                    for i in range(len(lista)):
                        baseDatos2 [j] = {'cedula':lista[j][0],'nombre':lista[j][1],'apellido':lista[j][2],'cargo':lista[j][3],'salario':lista[j][4]}
                        j=j+1
                   
                    if lista is None:
                        return redirect("/administrador")
                    else:
                        return render_template('base-lista-empleados.html',
                                tipo_user=tipo_user,
                                id_user=id_user,
                                baseDatos=baseDatos2,
                                nombre=nombre
                                )

    except:
        con.rollback()

        return redirect("/administrador")       
    # Lista = {}
    # if tipo_user == 2:
    #     for Actusuario in baseDatos:
    #         if nombre != baseDatos.get(Actusuario).get('nombre') and baseDatos.get(Actusuario).get('rol') != 3:
    #             Lista[Actusuario] = baseDatos.get(Actusuario)
    # else:
    #     for Actusuario in baseDatos:
    #         if nombre != baseDatos.get(Actusuario).get('nombre'):
    #             Lista[Actusuario] = baseDatos.get(Actusuario)
            
    

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
    try:
        with sqlite3.connect("SGE") as con:
            cur= con.cursor()
            cur.execute("delete from empleado where cedula=?;",[id_usuario])#sentencia  
            con.commit()
            return redirect('/lista-empleados')
              
    except:
            con.rollback()
    
    return redirect('/lista-empleados')


@app.route('/generar_retroalimentación/<int:id_usuario>', methods = ["POST"])
def generar_retroalimentación (id_usuario):
    if request.method == 'POST':
        print(id_usuario)
        fecha = request.form['Fecha']
        fecha = fecha.replace("/", "-")
        retroalimentacion= request.form['retroalimentacion-text']
        puntaje = float(request.form['puntaje'])
        try:
            with sqlite3.connect("SGE") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO retroalimentacion (id_empleado,retroalimentacion,puntaje,nombre_generador,fecha_de_creacion) VALUES (?,?,?,?,?)",(int(id_usuario),retroalimentacion,puntaje,"",fecha)).fetchone()
                con.commit()
        except Exception:
            print(Exception.args[0])
            con.rollback()
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

if __name__ == "__main__":
    app.run(debug=True)
