"""
Tests unitaires pour l'application Flask
"""
import unittest
from unittest.mock import patch, MagicMock
from app import app


class TestFlaskApp(unittest.TestCase):
    """Classe de tests pour l'application Flask"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.redis')
    def test_home_route_success(self, mock_redis):
        """Test du endpoint / avec succès"""
        # Configuration du mock Redis
        mock_redis.incr.return_value = 5

        # Appel de la route
        response = self.client.get('/')

        # Vérifications
        # ERREUR VOLONTAIRE : on attend 404 au lieu de 200 pour faire échouer le test
        self.assertEqual(response.status_code, 404)  # ← ERREUR ICI
        self.assertIn(b'Bonjour', response.data)
        self.assertIn(b'5', response.data)
        mock_redis.incr.assert_called_once_with('hits')

    @patch('app.redis')
    def test_home_route_redis_error(self, mock_redis):
        """Test du endpoint / avec erreur Redis"""
        # Simulation d'une erreur Redis
        mock_redis.incr.side_effect = Exception("Redis connection failed")

        # Appel de la route
        response = self.client.get('/')

        # Vérifications
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Erreur de connexion', response.data)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_container_id_display(self, mock_hostname, mock_redis):
        """Test de l'affichage de l'ID du conteneur"""
        # Configuration des mocks
        mock_redis.incr.return_value = 1
        mock_hostname.return_value = "test-container-123"

        # Appel de la route
        response = self.client.get('/')

        # Vérifications
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test-container-123', response.data)

    def test_app_exists(self):
        """Test que l'application Flask existe"""
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        """Test que le mode testing est activé"""
        self.assertTrue(self.app.config['TESTING'])


if __name__ == '__main__':
    # Exécution des tests avec un rapport détaillé
    unittest.main(verbosity=2)
