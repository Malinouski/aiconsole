import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { TopBar } from '@/components/TopBar';
import { PlusSmallIcon } from '@heroicons/react/24/outline';
import { MaterialItem } from '@/components/MaterialItem';
import { useAICStore } from '@/store/AICStore';

export function MaterialsPage() {
  const fetchMaterials = useAICStore((state) => state.fetchMaterials);
  const materials = useAICStore((state) => state.materials);

  useEffect(() => {
    fetchMaterials();
  }, []);

  return (
    <div className="App flex flex-col h-screen fixed top-0 left-0 bottom-0 right-0 bg-gray-800/95 text-stone-400">
      <TopBar />

      <Link to="/materials/new" className="absolute bottom-5 right-5">
        <button className="bg-primary  text-black/80 font-bold flex items-center justify-center  rounded-full hover:bg-primary-light">
          <PlusSmallIcon className="h-16 w-16" />
        </button>
      </Link>

      <div className="flex flex-row h-full overflow-y-auto">
        <div className="flex flex-col p-6 gap-4">
          {materials &&
            materials.map((material) => (
              <MaterialItem
                id={material.id}
                usage={material.usage}
                key={material.id}
              />
            ))}
        </div>
      </div>
    </div>
  );
}