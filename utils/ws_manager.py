from fastapi import WebSocket

class WSManager:
    """
    Manager połączeń WebSocket dla poszczególnych ankiet.

    Utrzymuje listę aktywnych połączeń dla każdego `poll_id` i pozwala
    na broadcast wiadomości do wszystkich klientów powiązanych z ankietą.
    """

    def __init__(self):
        """
        Inicjalizuje manager z pustym słownikiem połączeń.
        """
        # poll_id -> list[WebSocket]
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, poll_id: str, websocket: WebSocket):
        """
        Akceptuje nowe połączenie WebSocket i dodaje je do listy połączeń dla danej ankiety.

        :param poll_id: Identyfikator ankiety.
        :type poll_id: str
        :param websocket: Obiekt połączenia WebSocket.
        :type websocket: fastapi.WebSocket
        """
        await websocket.accept()
        if poll_id not in self.connections:
            self.connections[poll_id] = []
        self.connections[poll_id].append(websocket)

    def disconnect(self, poll_id: str, websocket: WebSocket):
        """
        Usuwa połączenie WebSocket z listy aktywnych połączeń danej ankiety.

        :param poll_id: Identyfikator ankiety.
        :type poll_id: str
        :param websocket: Obiekt połączenia WebSocket do usunięcia.
        :type websocket: fastapi.WebSocket
        """
        if poll_id in self.connections and websocket in self.connections[poll_id]:
            self.connections[poll_id].remove(websocket)

    async def broadcast(self, poll_id: str, message: dict):
        """
        Wysyła wiadomość do wszystkich połączonych klientów danej ankiety. Wywołuje to aktualizacje ankiety lokalnie u każdego klienta.

        :param poll_id: Identyfikator ankiety.
        :type poll_id: str
        :param message: Wiadomość do wysłania (słownik JSON).
        :type message: dict
        """
        conns = self.connections.get(poll_id, [])
        for ws in conns:
            try:
                await ws.send_json(message)
            except:
                print("Jakiś błąd")


# Globalny manager WS
ws_manager = WSManager()
