import lupa

lua_code_init = '''
      %s = {}
      function %s:new() 
         o = {}
         print "coucou"
         setmetatable(o, self)
         self.__index = self
         return o
      end
      
      function %s:affect(v)
         print("affect |----> " .. v)
         self.value = v
      end

      function %s:OP(arg)
         for item in python.iter(arg) do
            print(item)
         end
      end

      return %s
    '''

class LuaFunc :
   def __init__(self, function, obj) :
      self.__function = function
      self.__obj = obj

   def __call__(self, *args, **kwargs):
#      print "c -->", args, kwargs
      nargs = [self.__obj]
      nargs.extend(args)
      return apply(self.__function, nargs, kwargs)

class LuaObject :
   def __init__(self, obj) :
      self.__obj = obj

      self.__dict__[ "affect" ] = LuaFunc( self.__obj.affect, self.__obj )
      self.__dict__[ "OP" ] = LuaFunc( self.__obj.OP, self.__obj )

class LuaClass :
   def __init__(self, lua, name) :
      self.__lua = lua
      self.__class = self.__lua.execute( lua_code_init % (name, name, name, name, name) )

      self.__obj = LuaObject( self.__class.new(self.__class) )

   def get_obj(self) :
      return self.__obj

   def __getattr__(self, *args, **kwargs) :
#      print "class -->", args, kwargs
      return getattr(self.__obj, *args)

def INIT() :
   return WM_L3

class WM_L3 :
   def __init__(self, vm, method, analysis) :
      self.__lua = lupa.LuaRuntime()
     
      x = analysis.get_op("&")

      o = LuaClass(self.__lua, "L3")
      #      print o

      o.affect( "toto" )

      o.OP( [ 5, 6, "ioo" ] )

      raise("ooops")

   def get(self) :
      return [ 900090903, 980978789, 656767, 7667 ]
   
   def set_context(self, values) :
      pass

