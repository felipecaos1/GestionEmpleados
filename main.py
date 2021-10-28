from flask import Flask, render_template,redirect, request
import sqlite3
import os 
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# creamos una "base de datos" con 3 usuarios
# baseDatos={
#     1:{'id':'e1','nombre':'Felipe','apellido':'Castro','rol':1},
#     2:{'id':'e2','nombre':'Camilo','apellido':'osorio','rol':1},
#     3:{'id':'a3','nombre':'Pepe','apellido':'cardona','rol':2},
#     4:{'id':'s4','nombre':'Maria','apellido':'perez','rol':3}
# }


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
            
                if registro !=None:
                    if check_password_hash(registro[2],formContraseña):#desencripto y calido contraseñ
                        session=True
                        registro2=cur.execute("select * from empleado where cedula = ?",[registro[0]]).fetchone()
                        nombre=registro2[1]
                        tipo_user=registro2[5]
                        id_user=registro2[0]
                        return redirect('/administrador')   
        except:
            con.rollback()
    
    return redirect('/')
   

@app.route('/administrador/<int:id_usuario>/',methods = ["GET"])
@app.route('/administrador',methods = ["GET"])
def administrador ():
    global session, tipo_user,id_user,nombre
    print(session)
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
    global tipo_user, session
    tipo_user=0
    session=False 

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
    usuario=[]
    #try:

    with sqlite3.connect("SGE") as con:
                #con.row_factory=sqlite3.Row
                cur= con.cursor()
                
                cur.execute("select * from empleado where cedula=?",[id_usuario])
                lista=cur.fetchone()
                cur.execute("select * from datos where id=?",[id_usuario])
                lista2=cur.fetchone()
                
                if lista is None:
                    return redirect("/administrador")
                else:
                    return render_template('base-info.html',
                            tipo_user=tipo_user,
                            id_user=id_user,
                            baseDatos=lista,
                            nombre=nombre,
                            usuario=lista2[1]

                            )

    #except:
        #con.rollback()

    return render_template('administrador.html',
        tipo_user=tipo_user,
        id_user=id_user,
        nombre=nombre
        )    
    

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
    FechaTerminacion= request.form['crear-fecha-termino']
    Rol= request.form['tipo-rol']
    Salario= float(request.form['crear-salario'])
    dependencia= request.form['crear-dependencia']
    global valorId 
    global baseDatos
    if Rol == 'empleado':
        Rol2 = 1
        subId = 'e'+ str(valorId)
    elif Rol == 'administrador':
        Rol2= 2
        subId = 'a'+ str(valorId)
    else:
        Rol2 = 3   
        subId = 's'+ str(valorId)
    
    # conexion a la base de datos ( por terminar) 
    try:
        with sqlite3.connect("SGE") as con:#conectarse a la base de dto oficial
            cur= con.cursor()
            cur.execute("insert into empleado(cedula,nombre,apellido,cargo,salario,rol_id,fechainicio,fechatermino,tipocontrato,dependencia) values (?,?,?,?,?,?,?,?,?,?)",(int(cedula),nombreU,apellido,Rol,Salario,Rol2,fechaIngreso,FechaTerminacion,tipocontrato,dependencia))#sentencia y valores terminar 
            cur.execute("insert into datos(id,usuario,contrasena) values(?,?,?)",(int(cedula),usuario,contra_cifrada))
            con.commit()
            valorId +=1
            return redirect("/administrador")
                
    except:
        con.rollback()
        return redirect("/administrador")

    #baseDatos [valorId] = {'id':subId,'nombre':nombreU,'apellido':apellido,'rol':Rol}
    
    

@app.route('/lista-empleados',methods=["GET"])
def listarEmpleados():
    baseDatos2={}
    global id_user, tipo_user
    try:

        with sqlite3.connect("SGE") as con:
                    #con.row_factory=sqlite3.Row
                    cur= con.cursor()
                    print(id_user)
                    if tipo_user==2:
                        cur.execute("select * from empleado where cedula!=? and rol_id=1",[id_user])
                    else:
                        cur.execute("select * from empleado where cedula!=?",[id_user])
                    lista=cur.fetchall()
                    j=0
                    for i in range(len(lista)):
                        baseDatos2 [j] = {'cedula':lista[j][0],'nombre':lista[j][1],'apellido':lista[j][2],'cargo':lista[j][3],'salario':lista[j][4],'fechaingreso':lista[j][6],'fechatermino':lista[j][7],'tipocontrato':lista[j][8],'dependencia':lista[j][9]}
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
            cur.execute("delete from datos where id=?;",[id_usuario])
            con.commit()
            return redirect('/lista-empleados')
              
    except:
            con.rollback()
    
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

if __name__ == "__main__":
    app.run(debug=True)
