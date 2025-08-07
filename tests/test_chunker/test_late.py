from pprint import pp

from chonkie import Visualizer

from core.chunker.chonk.late import ChonkLateChunker
import pytest

vis = Visualizer()

TEST_TEXT = '''
Artificial Intelligence (AI) represents one of the most transformative technologies of our time. From its theoretical foundations laid by pioneers like Alan Turing and John McCarthy to today's sophisticated machine learning systems, AI has evolved dramatically.

The field encompasses various subdomains including machine learning, natural language processing, computer vision, and robotics. Machine learning, in particular, has gained tremendous traction with the development of neural networks and deep learning architectures.

Neural networks, inspired by the human brain's structure, consist of interconnected nodes that process and transmit information. Deep learning networks with multiple layers can learn complex patterns and representations from vast amounts of data.

One of the most significant breakthroughs in recent years has been the development of large language models (LLMs) like GPT, BERT, and T5. These models demonstrate remarkable capabilities in understanding and generating human-like text across diverse tasks.

Applications of AI span numerous industries. In healthcare, AI assists in medical diagnosis, drug discovery, and personalized treatment plans. In finance, it powers algorithmic trading, fraud detection, and risk assessment. Transportation benefits from autonomous vehicles and traffic optimization systems.

However, AI development also raises important ethical considerations. Issues such as bias in algorithms, privacy concerns, job displacement, and the need for AI transparency and explainability are actively being addressed by researchers and policymakers.

The future of AI holds immense promise. Emerging trends include federated learning, which enables training models across distributed data sources while preserving privacy. Quantum machine learning explores the intersection of quantum computing and AI algorithms.

As AI continues to advance, it will likely become even more integrated into our daily lives, transforming how we work, communicate, and solve complex problems. The key lies in developing AI systems that are not only powerful but also responsible, ethical, and beneficial to humanity.
'''

@pytest.mark.filterwarnings("ignore:")
def test_late_chunker():
    chunker = ChonkLateChunker(chunk_size=128)
    result = chunker.chunk(TEST_TEXT)

    pp("-" * 20 + "late chunker basic result:" + "-" * 20)
    vis.print(chunker.chunker.chunk(TEST_TEXT))  # type: ignore
    pp("-" * 20 + "late chunker basic finish" + "-" * 20)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(chunk, str) for chunk in result)
