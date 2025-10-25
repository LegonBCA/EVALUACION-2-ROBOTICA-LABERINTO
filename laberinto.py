# No es necesario importar 'mbot2', ya viene dentro de 'cyberpi'
import time
import mbuild
import cyberpi

# --- Variables de Estado y Movimiento ---
estado = 0  # 0 = Detenido, 1 = Avanzando
camino_Derecha = 0
camino_Izquierda = 0
velocidad = 60
pared = 7
contador_pared = 0
ladoB = 0
#contador de colores
morado = 0
amarillo = 0
azul = 0
verde = 0

# --- Variables para el CONTADOR de tiempo ---
tiempo_inicio = 0
contador_activo = False

# --- Configuración Inicial ---
cyberpi.mbot2.drive_speed(0, 0) # CORREGIDO: Inicia detenido
cyberpi.console.clear()
cyberpi.console.print("Presiona B para")
cyberpi.console.print("iniciar...")


while True:
    
    # --- SECCIÓN 1: CONTROL DE ESTADO (BOTONES) ---
    
    if cyberpi.controller.is_press("b"):
        # Si presionas 'b', enciende el robot (estado = 1)
        estado = 1
        
        # --- LÓGICA DEL CONTADOR (INICIO) ---
        # Si el contador no estaba activo, lo iniciamos
        if not contador_activo:
            tiempo_inicio = time.ticks_ms()
            contador_activo = True
            cyberpi.console.clear()
            cyberpi.console.print("¡Contador iniciado!")
        
        # Espera a que sueltes el botón
        while cyberpi.controller.is_press("b"):
            pass
            
    elif cyberpi.controller.is_press("a"):
        # Si presionas 'a', apaga el robot (estado = 0)
        estado = 0
        
        # --- LÓGICA DEL CONTADOR (DETENER) ---
        if contador_activo:
            contador_activo = False
            cyberpi.console.clear()
            cyberpi.console.print("Paro manual.")
            
        # Espera a que sueltes el botón
        while cyberpi.controller.is_press("a"):
            pass

            
    # --- SECCIÓN 2: ACCIÓN DEL ROBOT (SEGÚN EL ESTADO) ---
    
    if estado == 1:
        
        # --- AÑADIDO: 1. REVISAR LÍNEA NEGRA (FIN DEL CONTADOR) ---
        color_sensor_1 = mbuild.quad_rgb_sensor.get_color_sta(1)
        color_sensor_2 = mbuild.quad_rgb_sensor.get_color_sta(2)
        color_sensor_3 = mbuild.quad_rgb_sensor.get_color_sta(3)
        color_sensor_4 = mbuild.quad_rgb_sensor.get_color_sta(4)

        if color_sensor_2 == "black" or color_sensor_3 == "black":
            # ¡LÍNEA NEGRA DETECTADA!
            
            # a. Detener el robot
            estado = 0
            cyberpi.mbot2.drive_speed(0, 0) # CORREGIDO
            
            # b. Calcular y mostrar el tiempo
            if contador_activo:
                tiempo_fin = time.ticks_ms()
                duracion_ms = time.ticks_diff(tiempo_fin, tiempo_inicio)
                duracion_segundos = duracion_ms / 1000
                
                cyberpi.console.clear()
                cyberpi.console.println("Tiempo: {:.1f}s".format(duracion_segundos))
                
                cyberpi.console.println("Color Azul: {}".format(azul))
                cyberpi.console.println("Color morado: {}".format(morado))
                cyberpi.console.println("Color amarillo: {}".format(amarillo))
                cyberpi.console.println("Color verde: {}".format(verde))
                
                contador_activo = False
                
            cyberpi.audio.play("hit")
        
        # --- 2. SI NO HAY LÍNEA NEGRA, CONTINUAR CON EVASIÓN DE OBSTÁCULOS ---
        else:
            distanciaO = mbuild.ultrasonic2.get(1)
            
            if distanciaO < pared:
                # --- LÓGICA DE OBSTÁCULOS (Corregida) ---
                contador_pared = contador_pared + 1
                cyberpi.mbot2.drive_speed(0,0) # CORREGIDO
                time.sleep(0.4)
                cyberpi.mbot2.turn(92) #gira a la derecha # CORREGIDO
                camino_Derecha = mbuild.ultrasonic2.get(1)
                cyberpi.mbot2.turn(183) #gira a la izquierda # CORREGIDO
                camino_Izquierda = mbuild.ultrasonic2.get(1)
                
                #SECCIÓN DE OPCIÓN
                if contador_pared == 3:
                    cyberpi.mbot2.turn(181)
                     
                else:
                    if ladoB > 0
                        cyberpi.mbot2.turn(-92)
                        
                        if camino_Izquierda > camino_Derecha:
                            pass
                        else:
                            cyberpi.mbot2.turn(181) # CORREGIDO
                            
            else:
                # Sin obstáculo, avanza
                # CORREGIDO: (velocidad, velocidad) es avanzar recto
                cyberpi.mbot2.drive_speed(velocidad, -(velocidad)) 
                if cyberpi.controller.is_press("middle"):
                    ladoB = ladoB +1
                
                if color_sensor_1 == "yellow" or color_sensor_2 == "yellow" or color_sensor_3 == "yellow" or color_sensor_4 == "yellow":
                    amarillo = amarillo + 1
                    cyberpi.led.on("yellow")
                if color_sensor_1 == "blue" or color_sensor_2 == "blue" or color_sensor_3 == "blue" or color_sensor_4 =="blue":
                    azul = azul + 1
                    cyberpi.led.on("blue")
                if color_sensor_1 == "purple" or color_sensor_2 == "purple" or color_sensor_3 == "purple" or color_sensor_4 == "purple":
                    morado = morado + 1
                    cyberpi.led.on("purple")
                if color_sensor_1 == "green" or color_sensor_2 == "green" or color_sensor_3 == "green" or color_sensor_4 == "green":
                    verde = verde + 1
                    cyberpi.led.on("green")
                    
    # Si el estado es "Detenido" (0)...
    else:
        # Detiene el robot
        cyberpi.mbot2.drive_speed(0, 0) # CORREGIDO
        
    # Pequeña pausa para que el bucle sea estable
    time.sleep(0.02)