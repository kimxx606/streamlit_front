import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# 상위 디렉토리를 시스템 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 테스트할 모듈 임포트
from service_page.common import call_api

class TestCommonModule(unittest.TestCase):
    """공통 모듈에 대한 테스트 클래스"""
    
    @patch('service_page.common.requests.post')
    def test_call_api_success(self, mock_post):
        """API 호출 성공 시 테스트"""
        # Mock 응답 설정
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "테스트 응답입니다."}
        mock_post.return_value = mock_response
        
        # API 호출
        result = call_api(
            api_url="http://test-api.com/endpoint",
            query="테스트 질문입니다.",
            language="ko"
        )
        
        # 결과 검증
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["response"], "테스트 응답입니다.")
        
        # 올바른 파라미터로 호출되었는지 검증
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["url"], "http://test-api.com/endpoint")
        
        # 요청 데이터 검증
        payload = json.loads(kwargs["data"])
        self.assertEqual(payload["query"], "테스트 질문입니다.")
        self.assertEqual(payload["language"], "ko")
    
    @patch('service_page.common.requests.post')
    def test_call_api_error(self, mock_post):
        """API 호출 실패 시 테스트"""
        # Mock 응답 설정
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        # API 호출
        result = call_api(
            api_url="http://test-api.com/endpoint",
            query="테스트 질문입니다.",
            language="ko"
        )
        
        # 결과 검증
        self.assertFalse(result["success"])
        self.assertIn("API 오류: 500", result["error"])
        self.assertEqual(result["details"], "Internal Server Error")
    
    @patch('service_page.common.requests.post')
    def test_call_api_timeout(self, mock_post):
        """API 호출 타임아웃 시 테스트"""
        # 타임아웃 예외 발생
        mock_post.side_effect = TimeoutError("Connection timed out")
        
        # API 호출
        result = call_api(
            api_url="http://test-api.com/endpoint",
            query="테스트 질문입니다.",
            language="ko"
        )
        
        # 결과 검증
        self.assertFalse(result["success"])
        self.assertIn("오류가 발생했습니다", result["error"])
    
    @patch('service_page.common.requests.post')
    def test_call_api_with_history(self, mock_post):
        """대화 기록이 있는 경우 API 호출 테스트"""
        # Mock 응답 설정
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "대화 기록 테스트 응답입니다."}
        mock_post.return_value = mock_response
        
        # 대화 기록 설정
        history = [
            {"role": "user", "content": "이전 질문입니다."},
            {"role": "assistant", "content": "이전 응답입니다."}
        ]
        
        # API 호출
        result = call_api(
            api_url="http://test-api.com/endpoint",
            query="새로운 질문입니다.",
            language="ko",
            history=history
        )
        
        # 결과 검증
        self.assertTrue(result["success"])
        
        # 요청 데이터 검증
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs["data"])
        self.assertEqual(payload["history"], history)

if __name__ == '__main__':
    unittest.main() 