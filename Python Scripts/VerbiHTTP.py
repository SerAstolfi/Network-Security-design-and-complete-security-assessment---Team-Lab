import http.client

# host = "192.168.20.10"
# port = 80 #Porta di default per HTTP
# path= "/dvwa/"

# payload_POST = b"username=admin&password=password&Login=Login"
# payload_PUT = b"data=test_put_update"
content_type = "application/x-www-form-urlencoded" #Header per POST e PUT 

def verifica_Http(host,port,path,custom_payload) : 
    report_data_http = []
    verbi_test = ["GET","DELETE","POST","PUT"]
    payload_bytes= None
    payload_sent_str = "Non presente"

    if custom_payload : 
        try : 
            payload_bytes = custom_payload.encode('utf-8')
            payload_sent_str = custom_payload
        except Exception : 
            payload_sent_str = "Errore Codifica Payload"


    # try : 
    #     conn = http.client.HTTPConnection(host,port,timeout=5)
    # except Exception as error : 
    #     print(f"Errore durante inizializzazione connessione : {error}")
    #     report_data_http.append({"Verbo" : "INITIALIZATION", "Codice_Stato": "non presente", "Dettaglio_Risposta": "Errore Connessione", "URL_Testato": f"http://{host}:{port}", "Payload": "Non presente"})
    #     return report_data_http
    
    for verbo in verbi_test : 
        #Variabili per payload e headers
        body = None
        headers={}
        payload_da_usare = "Non presente"
        if verbo == "POST" or verbo == "PUT" :
            if payload_bytes: 
                body = payload_bytes
                headers = {"Content-Type" : content_type}
                payload_da_usare = payload_sent_str
            else : 
                payload_da_usare="POST/PUT richiesto,payload vuoto"
        
        risultato = {"Verbo":verbo , "URL_Test":f"http://{host}:{port}{path}","Codice_Stato":"non presente","Dettaglio_Risposta" : "non presente" , "Payload" : payload_da_usare}

        conn =None
        try : 
            conn = http.client.HTTPConnection(host,port,timeout=5)
            conn.request(verbo,path,body=body,headers=headers)
            response = conn.getresponse()
            risultato["Codice_Stato"] = response.status
            if 200 <= risultato["Codice_Stato"] < 400 :
                risultato["Dettaglio_Risposta"] = f"Successo : {response.reason}" 
            elif verbo == "OPTIONS" and response.status == 200:
                risultato["Dettaglio_Risposta"] = f"Metodi Abilitati : {response.getheader('Allow','Non trovato')}"
            else : 
                risultato["Dettaglio_Risposta"] = response.reason
            
            print(f"{verbo:<8} : Stato{risultato['Codice_Stato']} - {risultato['Dettaglio_Risposta'][:40]}...")
        except ConnectionRefusedError: 
            risultato["Dettaglio_Risposta"] = "Connessione Fallita"
            print(f"{verbo}:{risultato['Dettaglio_Risposta']}")
        except Exception as error :
            risultato ["Dettaglio_Risposta"] = f"Errore generico {str(error)}"
        finally :
            if conn : 
                 conn.close()


        report_data_http.append(risultato)



    return report_data_http

if __name__ == "__main__":
    input_host = input(f"Inserisci l'IP del server(default : 192.168.20.10): ")
    input_port = input("Inserisci la porta(default : 80)")
    try : 
        input_port=int(input_port)
    except ValueError : 
        input_port=80
    input_path = input("Inserisci il Path(es. /dvwa/ -default : /):")
    custom_payload = input("Inserisci il Payload(Es. username=a&password=b)o lascia vuoto: ")
    risultati_test = verifica_Http(input_host,input_port,input_path,custom_payload)
    
    for risultato in risultati_test:
        payload_disp = ""
        if risultato.get('Payload') not in ['Non presente',None,'POST/PUT richiesto, payload vuoto'] : 
            payload_disp = f" (Payload: {risultato['Payload']})"  
        print(f"[{risultato['Verbo']:<8}] Stato: {risultato['Codice_Stato']} | Dettaglio: {risultato['Dettaglio_Risposta']}{payload_disp}")
    
