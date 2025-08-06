from pprint import pp

from core.chunker.chonk.agentic import AgenticChunker

TEST_STR = '''
# 深入探索：大型语言模型与检索增强生成（RAG）

## 什么是检索增强生成（RAG）？
检索增强生成（Retrieval-Augmented Generation，简称RAG）是一种先进的人工智能技术，它将大型语言模型（LLM）的强大生成能力与外部知识库的精确检索能力相结合。简单来说，当模型需要回答一个问题或生成一段文本时，它首先会从一个庞大的数据源（如维基百科、公司内部文档、数据库等）中检索出最相关的几段信息。然后，它将这些检索到的信息作为上下文，连同原始问题一起，提供给语言模型，从而生成一个信息更准确、内容更丰富、更不容易“胡说八道”的回答。这种方式有效地缓解了LLM知识陈旧和产生幻觉的问题。

RAG的核心优势在于它的动态性和可追溯性。由于知识库可以随时更新，RAG系统能够获取最新的信息，这是静态训练的LLM无法比拟的。同时，因为答案是基于检索到的特定文档生成的，我们可以很容易地追溯到信息的来源，增加了系统的透明度和可信度。

## RAG面临的挑战与Agentic Chunker的角色
尽管RAG非常强大，但在实际应用中也面临诸多挑战，其中“分块（Chunking）”策略是至关重要的一环。如果分块做得不好，检索阶段的效果将大打折扣，最终影响生成质量。传统的固定大小分块方法，比如简单地每1000个字符切一刀，很容易将一个完整的语义单元（比如一个关键定义或一个复杂的逻辑论证）硬生生地切开，导致检索到的上下文信息不完整，模型也就无法准确理解。想象一下，一个关键步骤的解释被分在了两个不同的块里，检索系统可能只找到了其中一半，那模型的回答必然是片面的。为了解决这个问题，智能分块技术应运而生。这里的Agentic Chunker就是一个很好的例子，它利用语言模型自身的理解能力来寻找文本中最自然的断点。它不仅仅是看字符数，更是去理解句子结构、段落主题和逻辑关系，力求在不超过设定长度（如1024个字符）的前提下，保持每个分块的语义完整性。这对于处理复杂的长篇文档、法律合同或者技术手册尤为重要，因为这些文档中的信息关联性极强，任何不恰当的分割都可能导致严重的理解偏差。一个优秀的Agentic Chunker能够显著提升RAG系统的“召回率”和“精确率”，是构建高效、可靠的知识问答系统的基石。

## RAG系统的关键步骤
一个典型的RAG系统通常包含以下几个核心步骤：
1.  **数据索引（Indexing）**: 将原始文档（如PDF, TXT, HTML文件）进行预处理，包括清洗、分块（Chunking），然后使用编码模型（Encoder）将每个文本块转换成向量（Vector Embeddings），并存入向量数据库中。
2.  **检索（Retrieval）**: 当用户提出问题时，同样将问题文本转换成向量，然后在向量数据库中进行相似度搜索，找出与问题向量最相近的N个文本块。
3.  **生成（Generation）**: 将检索到的N个文本块作为上下文信息，与用户的原始问题一起，构建成一个完整的提示（Prompt），然后送入大型语言模型进行最终的回答生成。

## 代码示例：一个简单的RAG查询函数
下面是一个伪代码，演示了RAG的基本逻辑。一个好的chunker应该尽量保持这样的代码块完整。

```python
def simple_rag_query(query: str, vector_db: VectorDB, llm: LLM):
    # 1. Retrieve relevant text chunks
    retrieved_chunks = vector_db.search(query, top_k=3)
    
    # 2. Build the prompt with context
    context = "\n".join([chunk.text for chunk in retrieved_chunks])
    prompt = f"""
    Based on the following context, please answer the question.
    Context:
    {context}
    
    Question: {query}
    
    Answer:
    """
    
    # 3. Generate response using the LLM
    response = llm.generate(prompt)
    return response
'''


def test_langchunker():
    chunker = AgenticChunker()
    result: list[str] | list[list[str]] = chunker.chunk(TEST_STR)

    pp("-" * 20 + "chunker result:" + "-" * 20)
    pp(result)
    pp("-" * 20 + "chunker  finish" + "-" * 20)

    assert result is not None
