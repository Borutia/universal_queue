from server import api


class TestAPI:
    async def get_application(self):
        return api.setup_app()

    async def test_add_queue(self):
        data = {"queue": "example"}
        headers = {'content_type': 'application/json'}
        response = await self.client.post(
            '/queue',
            data=data,
            headers=headers,
        )
        assert response.status == 200
        response_data = {'queue_id': 1}
        assert response_data == response.data

    async def test_add_task(self):
        data = {
            "queue": "example",
            "kwargs": {
                "param1": 1,
                "param2": 2
            }
        }
        response = await api.add_task(data)
        assert response.status == 201
        response_data = {'task_id': 1}
        assert response_data == response.data
