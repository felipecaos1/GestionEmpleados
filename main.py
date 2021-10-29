from flask import Flask, render_template,redirect, request
import sqlite3
import os 
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

retroalimentacionEmpleados ={}
#VARIABLES
tipo_user = ''
id_user = ''
nombre = ''
valorId = 6
session=False #verifica si esta loguiado
clavemala=""
#1:empleado
#2:administrador
#3:Superadminstrador

@app.route('/',methods = ["GET","POST"])
def login():
    global clavemala

    return render_template("Login.html",mensaje=clavemala)

@app.route('/ingreso', methods = ["POST"]) #aca se valida el usuario
def ingreso():
    global tipo_user,id_user, nombre, session,clavemala
    
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
                        clavemala=""
                        return redirect('/administrador')   
                    else:
                        clavemala="Usuario o Clave incorrecta"
                else:
                    clavemala="Usuario o Clave incorrecta"

        except:
            con.rollback()

    return redirect('/')
    
    
   

# @app.route('/administrador/<int:id_usuario>/',methods = ["GET"])
@app.route('/administrador',methods = ["GET"])
def administrador ():
    global session, tipo_user,id_user,nombre
  
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
    baseDatos4={}
    try:
        with sqlite3.connect("SGE") as con:
            cur= con.cursor()
            data = cur.execute("SELECT * FROM retroalimentacion where id_empleado=?;",[id_usuario]).fetchall()#sentencia  
          
            con.commit()

            if data is None:
                return redirect("/administrador")
            else:
                j=0
                for i in range(len(data)):
                    baseDatos4 [j] = {'id':data[j][0],'retro':data[j][2],'fecha':data[j][5],'puntaje':data[j][3],'autor':data[j][4]}
                    j=j+1
                return render_template('base-Retroalimentacion.html',
                        tipo_user=tipo_user,
                        id_user=id_user,
                        baseDatos=baseDatos4,
                        nombre=nombre
                        )
              
    except:
            con.rollback()
    
    return render_template('base-Retroalimentacion.html',
    tipo_user=tipo_user,
    id_user=id_usuario,
    nombre=nombre,
    )


@app.route('/e_informacionpersonal/<id_usuario>', methods = ["GET"])
def e_informacionpersonal(id_usuario):
    usuario=[]
    global session
    if session:
        try:

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

        except:
            con.rollback()

        return render_template('administrador.html',
            tipo_user=tipo_user,
            id_user=id_user,
            nombre=nombre
            )    
    else:
        return redirect("/")    

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
    
    Salario= request.form['crear-salario']
    dependencia= request.form['crear-dependencia']
    global valorId 
    global baseDatos
   
    if Rol == 'Administrador':
        Rol2= 2
       
    elif Rol== 'SuperAdministrador':
         Rol2 = 3   
    else:
        Rol2 = 1   
        
    
    # conexion a la base de datos ( por terminar) 
    try:
        with sqlite3.connect("SGE") as con:#conectarse a la base de dto oficial
            cur= con.cursor()
            cur.execute("insert into empleado(cedula,nombre,apellido,cargo,salario,rol_id,fechainicio,fechatermino,tipocontrato,dependencia) values (?,?,?,?,?,?,?,?,?,?)",(int(cedula),nombreU,apellido,Rol,Salario,Rol2,fechaIngreso,FechaTerminacion,tipocontrato,dependencia))
            cur.execute("insert into datos(id,usuario,contrasena) values(?,?,?)",(int(cedula),usuario,contra_cifrada))
            con.commit()
            return redirect("/administrador")
                
    except:
        con.rollback()
        return redirect("/administrador")

    
    
    
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
                        lista=cur.fetchall()
                        cur.execute("select * from datos where id!=? ",[id_user])
                        datos=cur.fetchall()
                    else:
                        cur.execute("select * from empleado where cedula!=?",[id_user])
                        lista=cur.fetchall()
                        cur.execute("select * from datos where id!=?",[id_user])
                        datos=cur.fetchall()
                    
                    if lista is None:
                        return redirect("/administrador")
                    else:
                        j=0
                        for i in range(len(lista)):
                            baseDatos2 [j] = {'cedula':lista[j][0],'nombre':lista[j][1],'apellido':lista[j][2],'cargo':lista[j][3],'salario':lista[j][4],'fechaingreso':lista[j][6],'fechatermino':lista[j][7],'tipocontrato':lista[j][8],'dependencia':lista[j][9],"usuario":datos[j][1]}
                            j=j+1
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
    basedatos3={}
    try:
        with sqlite3.connect("SGE") as con:
                #con.row_factory=sqlite3.Row
                cur= con.cursor()
            
                if tipo_user==2:
                    cur.execute("select * from empleado join datos where cedula=? and id=?;",(buscar,buscar))
                    lista=cur.fetchall()
                    print(lista)
                    # cur.execute("select * from datos where id!=? ",[id_user])
                    # datos=cur.fetchall()
                else:
                    cur.execute("select * from empleado join datos where cedula=? and id=? and cedula!=?;",(buscar,buscar,id_user))
                    lista=cur.fetchall()
                    print(lista)
                    # cur.execute("select * from datos where id!=?",[id_user])
                    # datos=cur.fetchall()
                
                if lista is None :
                    return redirect("/administrador")
                else:
                    j=0
                    for i in range(len(lista)):
                        basedatos3 [j] = {'cedula':lista[j][0],'nombre':lista[j][1],'apellido':lista[j][2],'cargo':lista[j][3],'salario':lista[j][4],'fechaingreso':lista[j][6],'fechatermino':lista[j][7],'tipocontrato':lista[j][8],'dependencia':lista[j][9],"usuario":lista[j][11]}
                        j=j+1
                    return render_template('base-lista-empleados.html',
                            tipo_user=tipo_user,
                            id_user=id_user,
                            baseDatos=basedatos3,
                            nombre=nombre
                            )

    except:
        #pass
        return render_template('base-lista-empleados.html',
        tipo_user=tipo_user,
        id_user=id_user,
        baseDatos=basedatos3,
        nombre=nombre
        )

@app.route('/eliminar_empleado/<int:id_usuario>', methods = ["GET", "POST"])
def eliminar_empleado (id_usuario):
    #recibir el id del empleado donde se presiono eliminar para bucarlo en la base y eliminarlo 
    global session
    if session:
        try:
            with sqlite3.connect("SGE") as con:
                cur= con.cursor()
                cur.execute("delete from empleado where cedula=?;",[id_usuario])#sentencia  
                con.commit()
                cur.execute("delete from datos where id=?;",[id_usuario])
                con.commit()
                cur.execute("delete from retroalimentacion where id_empleado=?;",[id_usuario])
                con.commit()
                return redirect('/lista-empleados')
                
        except:
                con.rollback()
        
        return redirect('/lista-empleados')
    else:
        return redirect("/")


@app.route('/generar_retroalimentación/<int:id_usuario>', methods = ["POST"])
def generar_retroalimentación (id_usuario):
    #comentario
    global nombre,session
    if session:
        if request.method == 'POST':
            print(id_usuario)
            fecha = request.form['Fecha']
            fecha = fecha.replace("/", "-")
            retroalimentacion= request.form['retroalimentacion-text']
            puntaje = float(request.form['puntaje'])
            try:
                with sqlite3.connect("SGE") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO retroalimentacion (id_empleado,retroalimentacion,puntaje,nombre_generador,fecha_de_creacion) VALUES (?,?,?,?,?)",(int(id_usuario),retroalimentacion,puntaje,nombre,fecha)).fetchone()
                    con.commit()
            except Exception:
                print(Exception.args[0])
                con.rollback()
                return redirect('/lista-empleados')
        return redirect('/lista-empleados')
    else:
        return redirect("/")

@app.route('/editar_empleado/<int:id_usuario>', methods = ["POST"])
def editar_empleado (id_usuario):
    if request.method == 'POST':
        nombreU = request.form['editar-nombre']
        apellido= request.form['editar-apellido']
        
        usuario= request.form['editar-usuario']
        contrasena= request.form['editar-contraseña'] 
        contra_cifrada=generate_password_hash(contrasena) #esta es la contraseña que hay que guardar en la base de datos
        tipocontrato=request.form['editar-contrato']
        fechaIngreso= request.form['editar-fecha1']
        FechaTerminacion= request.form['editar-fecha2']
        Rol= request.form['editar-cargo']
        Salario= request.form['editar-salario']
        dependencia= request.form['editar-dependencia']

        
    
        if Rol == 'Administrador':
            Rol2= 2
        
        elif Rol== 'SuperAdministrador':
            Rol2 = 3   
        else:
            Rol2 = 1    
            
       # try:
        with sqlite3.connect("SGE") as con:#conectarse a la base de dto oficial
            cur= con.cursor()
            cur.execute("update empleado set nombre=?,apellido=?,cargo=?,salario=?,rol_id=?,fechainicio=?,fechatermino=?,tipocontrato=?,dependencia=? where cedula=?",[nombreU,apellido,Rol,Salario,Rol2,fechaIngreso,FechaTerminacion,tipocontrato,dependencia,id_usuario])
            con.commit()
            print("hola")
            print(contrasena)
            if contrasena=="sin modificar":
                print("entro")
                cur.execute("update datos set usuario=? where id=?",(usuario,id_usuario))
                con.commit()
            else:
                print("contra")
                cur.execute("update datos set usuario=?,contrasena=? where id=?",(usuario,contra_cifrada,id_usuario))
                con.commit()
                
            return redirect("/lista-empleados")
                
        #except:
           # con.rollback()
            #return redirect("/lista-empleados")
    return redirect("/lista-empleados")
        
#HASTA ACA ORGANIZADO////////////////////////////////////////////////////////////////////////////// 

if __name__ == "__main__":
    app.run(debug=True)
