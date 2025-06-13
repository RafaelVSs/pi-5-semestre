import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from ..schemas.classification_schema import PlayerStatsInput, ClassificationResult
from ..schemas.history_schema import HistoryCreate
from ..services.history_service import HistoryService


class ClassificationService:
    def __init__(self, model_path: Optional[str] = None):
        # Configuração do caminho do modelo
        self.model_path = model_path or str(
            Path(__file__).parent.parent / "IA_script" / "modelo_classificador_nba.joblib"
        )
        self.model = self._load_model()

        self.classification_messages = {
            "Superstar": "Parabéns! Você é um Superstar — tipo o LeBron ou o Curry! 🏆🔥",
            "All-Star": "Muito bom! Você é um All-Star — consistente e respeitado na liga. ⭐",
            "Role Player": "Você é um Role Player — essencial pro time, sempre contribuindo. 💪",
            "Reserva": "Você é um reserva — mas toda estrela começa do banco. Siga treinando! 🛋️"
        }

    def _load_model(self):
        """Carrega o modelo de classificação"""
        return joblib.load(self.model_path)

    async def classify_player(
            self,
            stats: PlayerStatsInput,
            player_name: str,
            user_id: int,
            history_service: HistoryService
    ) -> ClassificationResult:
        # Prepara e executa a classificação
        classification = self._predict_classification(stats)

        # Cria e salva o histórico
        history_data = self._prepare_history_data(
            stats=stats,
            player_name=player_name,
            classification=classification,
            user_id=user_id
        )

        await history_service.create_history(history_data)

        return self._prepare_classification_result(
            player_name=player_name,
            classification=classification
        )

    def _predict_classification(self, stats: PlayerStatsInput) -> str:
        """Executa a predição do modelo"""
        input_data = pd.DataFrame([{
            "Pos": stats.position,
            "PPG": stats.points_per_game,
            "APG": stats.assists_per_game,
            "RPG": stats.rebounds_per_game
        }])
        return self.model.predict(input_data)[0]

    def _prepare_history_data(
            self,
            stats: PlayerStatsInput,
            player_name: str,
            classification: str,
            user_id: int
    ) -> HistoryCreate:
        """Prepara os dados para o histórico"""
        return HistoryCreate(
            player_name=player_name,
            position=stats.position,
            average_points=stats.points_per_game,
            average_assists=stats.assists_per_game,
            average_rebounds=stats.rebounds_per_game,
            classification=classification,
            user_id=user_id
        )

    def _prepare_classification_result(
            self,
            player_name: str,
            classification: str
    ) -> ClassificationResult:
        """Prepara o resultado da classificação"""
        return ClassificationResult(
            player_name=player_name,
            classification=classification,
            message=self.classification_messages.get(classification, "Classificação desconhecida.")
        )