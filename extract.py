import cv2
import os

# Caminho da pasta com os vídeos
video_folder = "C:/UFAPE/TOPIA/visaoComputacional/Arson"
output_folder = "C:/UFAPE/TOPIA/visaoComputacional/Frames_Arson/"

# Criar pasta de saída, se não existir
os.makedirs(output_folder, exist_ok=True)

# Configurações para extrair MENOS frames
target_fps = 0.5  # Apenas 1 frame a cada 2 segundos (quanto menor, menos frames)
min_skip_frames = 10  # Mínimo de frames a pular (garante que não extraia muitos)

# Percorre os vídeos da pasta
for video_file in os.listdir(video_folder):
    video_path = os.path.join(video_folder, video_file)

    # Verifica se é um arquivo de vídeo
    if not video_file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        continue

    print(f"\nProcessando vídeo: {video_file}")

    # Captura de vídeo com OpenCV
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Erro ao abrir vídeo: {video_file}")
        continue

    # Obtém o FPS original do vídeo
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps <= 0:
        original_fps = 30  # Valor padrão se não conseguir detectar

    # Calcula quantos frames pular para atingir o target_fps
    skip_frames = int(original_fps / target_fps)
    
    # Garante um mínimo de frames pulados (para evitar muitos frames)
    if skip_frames < min_skip_frames:
        skip_frames = min_skip_frames

    print(f"FPS original: {original_fps:.2f} | FPS alvo: {target_fps} | Pulando {skip_frames} frames")

    frame_count = 0
    saved_frames = 0

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print(f"Fim do vídeo ou erro ao ler frame {frame_count}")
            break

        # Extrai frame apenas se estiver no intervalo desejado
        if frame_count % skip_frames == 0:
            safe_video_name = "".join(c for c in os.path.splitext(video_file)[0] if c.isalnum() or c in (' ', '_')).rstrip()
            frame_filename = f"{safe_video_name}_frame{saved_frames:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)

            if cv2.imwrite(frame_path, frame):
                print(f"Frame {frame_count} salvo: {frame_filename}")
                saved_frames += 1
            else:
                print(f"Erro ao salvar frame {frame_count}")

        frame_count += 1

    cap.release()
    print(f"Concluído: {video_file} | Frames extraídos: {saved_frames}")

print("\nExtração de frames concluída!")