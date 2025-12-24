from concurrent import futures
import logging
import os

import grpc

from parser import parser_pb2_grpc
from parser.grpc_parcer_server import WebsiteParserServicer
import traceback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

port = os.getenv('GRPC_PARSER_PORT', '50051')
num_workers = int(os.getenv('PARSER_NUM_WORKERS', '1'))

if __name__ == '__main__':
    try:
        servicer = WebsiteParserServicer(num_workers=num_workers)
        
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers))
        parser_pb2_grpc.add_WebsiteParserServicer_to_server(servicer, server)
        server.add_insecure_port(f'0.0.0.0:{port}')
        
        logger.info(f"gRPC Server started on port {port}")
        server.start()
        
        server.wait_for_termination()
            
    except Exception as e:
        logger.error(f"Shutting down server, Error: {e}")
        traceback.print_exc()
        server.stop(0)
        exit(1)
