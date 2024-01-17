def text_splitter_txt_zh(text: str, chunk_size: int, overlap: int) -> list[str]:
    """中文纯文本切割"""
    chunks = []
    index = 0
    while index < len(text):
        if index + chunk_size >= len(text):
            chunks.append(text[index + 1:])
            break
        end_index = index + chunk_size
        if end_index < len(text):
            while end_index > index and text[end_index] not in "。？！；\n":
                end_index -= 1
        if end_index == index:
            end_index = index + chunk_size
        chunks.append(text[index + 1: end_index + 1])
        overlap_index = end_index - overlap
        if overlap_index > index:
            while overlap_index > index and text[overlap_index] not in "。？！\n":
                overlap_index -= 1
            if overlap_index == index:
                overlap_index = end_index - overlap
        index = overlap_index
    return chunks
