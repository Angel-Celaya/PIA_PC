from pyhunter import PyHunter
from scapy.all import *
import subprocess
import argparse
import getpass
import modpia

if __name__=="__main__":
    description = """
    Para usar el cifrado:
        *Cifrar el mensaje con palabra clave:
            -msg "hola mundo" -pc "root"
        *Descifrar el mensaje con palabra clave:
            -msgc "lspeAqyrhs" -pc "root"
        *Descifrar el mensaje sin palabra clave:
            -msgc "lspeAqyrhs" 
            (Mostrara un listado de todas las posibles combinaciones
             y se proporcionara la al final el posible mensaje.)
    
    Para usar el escaner de puertos:
        *Escaneo basico:
            -ip 148.234.80.185
        *Indica un puerto especifico:
            -ip 148.234.80.185 -ports 22
        *Indica una lista de puertos:
            -ip 148.234.80.185 -ports 22,101,110,etc,

    Para usar web scraping:
        -url "https://www.muylinux.com/tag/debian/"
        (Mostrara opciones de lo que se puede usar como descargar imagenes,
         pdfs o ver los enlaces de la url proporcionada.)
    
    Para usar scapy:
    	-r 148.234.80.1/24
    	(Para ejecutar esta opcion tiene que estar en modo root)

    Para usar hunter:
        -dom uanl.mx
        (Se le pedira si key de la API de hunter)
    """
    parser = argparse.ArgumentParser(description='Descripcion de uso del programa', 
                                     epilog=description,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-msg',dest="msg",help='El mensaje, palabra, frase, etc.')
    parser.add_argument('-msgc',dest="msgc",help='El mensaje cifrado')
    parser.add_argument('-pc', dest="pc",help='Palabra clave para cifrar/decifrar')
    parser.add_argument("-ip", dest="ip",help='Una direccion ip de un dispositivo, servidor, etc.')
    parser.add_argument("-ports", dest="ports",help='Puertos TCP/UDP de una direccion',default="80,8080")
    parser.add_argument("-url", dest="url", help='El url de una pagina')
    parser.add_argument("-r", dest="rango",help="Rango de direcciones a escanear")
    parser.add_argument("-dom", dest="dom", help="Dominio a investigar")

    args=parser.parse_args()
    #---cifrar---#
    message=(args.msg)
    #---decifrar---#
    messagec=(args.msgc)
    #---clave--#
    clave=(args.pc)
    if clave!=None:
        key=len(clave)
    #--------------------Cifrar un mensaje dada una clave--------------------#
    if message!=None and clave!=None:
        modpia.ccon_clave(message,key)
    #--------------------Descifrar un mensaje dada una clave--------------------#
    if messagec!=None and clave!=None:
        modpia.dcon_clave(messagec,key)
    #--------------------Crackear un mensaje cifrado--------------------#
    if messagec!=None and clave==None:
        modpia.crack(messagec)

    #--------------------Escanear puertos--------------------#
    portlist = args.ports.split(',')
    targ=(args.ip)
    if targ != None:
        for i in range(len(portlist)):
            portlist[i]=int(portlist[i])
        modpia.checkPortsSocket(targ,portlist)

    #--------------------Web scraping--------------------#
    url=(args.url)
    if url != None:
        print("""
    Opciones:
        * Descargar imagenes    = img
        * Descargar PDFs        = pdf
        * Ver los enlaces       = link
                """)
        modpia.opcionwebscraping(url)   
    #------------------scapy------------------------------#
    scy=(args.rango)
    if scy != None:
    	try:
    	    modpia.ip_scan(scy)
    	except Exception as e:
    	    print("""
    Sin permisos, tiene que tener permisos de super usuario
	Ejemplo:
	sudo su
	[ghost@fedora folder]$ --> [root@fedora folder]#
	[root@fedora folder]# python PIA.py -r 192.168.100.1/24
	ó
	Ejemplo:
	sudo python PIA.py -r 192.168.100.1/24
	""")
    #------------------hunter------------------------------#
    orga=(args.dom)
    if orga!= None:
        apikey = getpass.getpass("Ingresa tu API key: ")
        hunter = PyHunter(apikey)
        datosEncontrados = hunter.domain_search(company=orga,
                                                limit=1, emails_type="personal")
        if datosEncontrados is None:
            exit()
        else:
            print(datosEncontrados)
            print(type(datosEncontrados))
            modpia.GuardarInformacion(datosEncontrados, orga)
    #--------------------bash-------------------------------------#
    else:
        script = subprocess.call('./tarea.sh')
        print(script)


