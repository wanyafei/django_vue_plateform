<template>
<div class="app-container">
  <!-- 搜索表单 -->
    <el-form
      ref="queryParams"
      :model="queryParams"
      size="small"
      :inline="true"
    >
      <el-form-item>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
        <!-- <el-button type="success" icon="el-icon-edit" :disabled="single" @click="handleUpdate">修改</el-button> -->
        <el-button
          type="danger"
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          >删除</el-button
        >
      </el-form-item>
      <el-form-item prop="report_name">
        <el-input
          v-model="queryParams.taskname"
          placeholder="定时任务名称"
          clearable
          style="width: 220px"
          @keyup.enter.native="showTask"
        />
         <el-select v-model="queryParams.project" placeholder="所属项目" style="width: 140px" >
           <el-option v-for="item in options" :key="item.prj_id" :label="item.prj_name" :value="item.prj_id"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showTask">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading"
              :data="taskList"
              border  
              @selection-change="handleSelectionChange"           
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column prop="taste_name" label="定时任务名称" min-width="40">
      <template slot-scope="scope"> {{ scope.row.fields.taste_name }} </template>
      </el-table-column>
      <el-table-column prop="data" label="所属项目" min-width="30">
      <template slot-scope="scope"> {{ get_map_prj(scope.row.fields.project) }} </template>
      </el-table-column>
      <el-table-column prop="case_num" label="执行时间" min-width="30">
      <template slot-scope="scope"> {{ scope.row.fields.taste_time }} </template>
      </el-table-column>
      <el-table-column prop="pass_num" label="状态" min-width="30">
      <template slot-scope="scope"> {{ status_change(scope.row.fields.status) }} </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="140">
      <template slot-scope="scope" >
            <el-dropdown size="small" style="margin-left: 10px;" split-button type="primary" >
            更多操作
            <el-dropdown-menu slot="dropdown" >
                <el-dropdown-item  @click.native="runonce(scope.row.pk,2)">执行一次</el-dropdown-item>
                <el-dropdown-item divided @click.native="run(scope.row.pk,scope.row.fields.status)">{{ transformstatus(scope.row.fields.status) }}</el-dropdown-item>
                <el-dropdown-item divided @click.native="handleupdate(scope.row.pk)">编辑</el-dropdown-item>
                <el-dropdown-item divided @click.native="handleDelete(scope.row.pk)">删除</el-dropdown-item>
                <el-dropdown-item divided @click.native="getnexttime(scope.row.pk)">下次执行时间</el-dropdown-item>  
            </el-dropdown-menu>
            </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <div class="sc-pagination-container">
     <ul >
      <el-pagination
        background
        layout="total,prev, pager, next"
        v-show="pagination.total>0"
        :total="pagination.total"
        :page-size="pagination.limit"
        @current-change="handleCurrentChange">
      </el-pagination>
     </ul>
    </div> 
    <!-- 表单弹窗 -->
    <el-dialog :title="dialog.title" :visible.sync="dialog.visible" width="600px">
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">

        <el-row>
          <el-col :span="18">
            <el-form-item label="任务名称" prop="taste_name">
              <el-input v-model="form.taste_name" placeholder="请输入任务名称"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
        <el-col :span="12">
            <el-form-item label="所属项目" prop="project">
              <el-select v-model="form.project" placeholder="请选择" @change="getenv_bypro">
                <el-option
                  v-for="item in options"
                  :key="item.prj_id"
                  :label="item.prj_name"
                  :value="item.prj_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属环境" prop="env">
              <el-select v-model="form.env" placeholder="请选择">
                <el-option
                  v-for="item in env_list"
                  :key="item.env_id"
                  :label="item.env_name"
                  :value="item.env_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          </el-row>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="任务描述"/>
        </el-form-item>
        <el-row>
            <el-form-item label="执行时间" prop="taste_time">
            <div class="block">
            <el-date-picker
                v-model="form.taste_time"
                type="datetime"
                format="yyyy-MM-dd HH:mm"
                value-format="yyyy-MM-dd HH:mm"
                placeholder="选择日期时间">
            </el-date-picker>
            </div>
            </el-form-item>
        </el-row>
         <el-row>
            <el-form-item label="获取计划" prop="plans">
              <el-button type="primary" @click="get_plan_by_proandenv(form.project,form.env)">获取用例</el-button>
              <el-checkbox-group v-model="def" format="changeStyle">
                <el-checkbox 
                    v-for="item in plan_list_by_proandenv"
                    :key="item.plant_id"
                    :label="item.plant_name"
                    @change="handleChange($event,item.plant_id)">
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
        <el-button @click="dialog.visible=false">取 消</el-button>
      </div>
    </el-dialog>
    <!-- 下次运行时间的弹框 -->
    <el-dialog :title="dialog_runtime.title" :visible.sync="dialog_runtime.visible" width="600px">
        <el-row>
            <el-col >{{dialog_runtime.text}}
            </el-col>
        </el-row>
        <el-row slot="footer">
            <el-button @click="dialog_runtime.visible=false">取 消</el-button>
        </el-row>
    </el-dialog>
    <!-- 运行一次弹框 -->
    <el-dialog :title="run_once.title" :visible.sync="run_once.visible" width="600px">
        <el-row>
            <el-form label-width="100px" :rules="rules">
            <el-form-item label="请选择用户:" prop='user'>
            <el-col>
              <el-select v-model="user" placeholder="请选择">
                <el-option
                  v-for="item in userlist"
                  :key="item.user_id"
                  :label="item.username"
                  :value="item.user_id"
                >
                </el-option>
              </el-select>
          </el-col>
          </el-form-item>
            </el-form>
        </el-row>
        <el-row slot="footer">
            <el-button type="primary" @click="handlerunonce">确 定</el-button>
            <el-button @click="run_once.visible=false">取 消</el-button>
        </el-row>
    </el-dialog>
  </div>
</template>
<script> 
import {getprj,get_project_interface_case_all} from '@/api/interface';
import {get_plan_by_proidandenvid} from '@/api/testplan';
import {getTask,add,detail,del,update,get_next_runtime,get_user_byprj,runonceurl,run_route} from '@/api/task'
export default {
  // name: 'test1',
  data () {
    return {
      row_id:undefined,
      taskList: [],
      //更多操作下拉展示的状态及状态码
      status:{
          status_label:undefined, 
          code:undefined
      },  
      user:undefined, //要执行接收邮件的用户
      userlist:[], //项目对应的用户
      loading: false,
      //默认非多选时【删除】按钮不可点
      multiple:true,
      //多选
      task_ids:[],
      plan_list_by_proandenv:[], //弹框中存放测试计划列表
      //v_model取此值，没有默认0值使回显报错
      def:[0],
      form: {
          task_id:undefined,
          taste_name: undefined,
          project:undefined,
          env: undefined,
          description: undefined,
          taste_time:undefined,
          plans:[]
        },
      rules: {
          taste_name: [
            {required: true, message: '任务名称不能为空', trigger: 'blur'}
          ],
          taste_time: [
            {required: true, message: '请选择执行时间', trigger: 'blur'}
          ],
          project:[
            {required:true,message:'请选择所属项目',trigger:'blur'}
          ],
          env: [
            {required: true, message: '请选择所属环境', trigger: 'blur'}
          ],
          description: [
            {required: false, message: '请输入接口描述', trigger: 'blur'}
          ],
          plans: [
            {required: true, message: '请选择对应测试计划', trigger: 'blur'}
          ],
          user: [
            {required: true, message: '请选择邮件收件人', trigger: 'blur'}
          ],
        },
      dialog: {
          title: undefined,
          visible: false,
          type: undefined  // type 操作类型：1-新增 2-修改
        },
      closeDialog() {
        this.dialog = {
          title: undefined,
          visible: false,
          type: undefined
        }
      },
      dialog_runtime:{
          title: '下次运行时间',
          visible: false,
          text:undefined
      },
      run_once:{
          title: '选择邮件接收用户',
          visible: false,
          type:undefined  // 2-运行一次 1.运行
      },
      options: [],  //项目list
      env_list:[], //环境list
      queryParams: {
          taskname:undefined,
          project:undefined
        },
      pagination: {
          page: 1,
          limit: 5,
          total: 0
        },
    }
  },
  mounted: function () {
    this.showTask()
    this.getprojectparm()
    // this.gettask()
  },
  methods: {
    showTask () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getTask(this.queryParams).then((response) => {
            this.taskList = response.data.data
            this.pagination.total=response.data.totalCount
        })
    },
    getenv_bypro(pro_id){
        const flag="get_env_by_prj_id"
        get_project_interface_case_all(pro_id,flag).then((response)=>{
        this.env_list=response.data
      })
    },
    transformstatus(val){
        let lab=""
        switch(val){
            case 0:
                lab="启动"
                break;
            case 1:
                lab="暂停"
                break;
            case 2:
                lab="重启"
                break;
            case 3:
                lab="暂停"
                break;
        }
        return lab
    },
    status_change(val){
        let lab=""
        switch(val){
            case 0:
                lab="STOP"
                this.status.code=1
                break;
            case 1:
                lab="RUNNING"
                this.status.code=2
                break;
            case 2:
                lab="PAUSE"
                this.status.code=3
                break;
            case 3:
                lab="RESUME"
                this.status.code=4
                break;
        }
        return lab
    },
    resetForm() {
        this.form = {
          task_id:undefined,
          taste_name: undefined,
          project:undefined,
          env: undefined,
          description: undefined,
          taste_time:undefined,
          plans:[]
        }
        if (this.$refs['form']) {
          this.$refs['form'].resetFields()
        }
      },
    handleAdd() {
        this.resetForm()
        this.dialog = {
          title: '新增任务',
          visible: true,
          type: 'add'
        }
      },
   getprojectparm(){
        getprj().then((response)=>{
          this.options=response.data
        })
    },
    //弹框中的【确定】方法
    handlerunonce(){
        if(this.run_once.type===2){
            runonceurl(this.user,this.row_id).then((response)=>{
                alert(response.message)
                this.run_once.visible=false
                this.showTask()
        })
        }else{
            const data={
            "flag":this.status.code,
            "user":this.user,
            "task_id":this.row_id
        }
        run_route(data).then((response)=>{
            alert(response.message)
            this.run_once.visible=false
            this.showTask()
        })
        }
        
    },
     //弹框中获取测试计划
    get_plan_by_proandenv(prj_id,env_id){
        const type="get_plan_by_prjandenv"
        get_plan_by_proidandenvid(prj_id,env_id,type).then((response)=>{
            this.plan_list_by_proandenv=response.data
        }) 
    },
    //弹框中用例多选时触发的事件,选项点击后push进form列表
    handleChange:function(e,plan_id) {
      if(e){
        this.form.plans.push(plan_id);
      }else{
        this.delete(plan_id);
      }
//       this.form.case_list=this.store_case
    },
    //获取下次执行时间
    getnexttime(task_id){
        get_next_runtime(task_id).then((response)=>{
            this.dialog_runtime.visible=true
            this.dialog_runtime.text=response.message
        })
    },
    //运行一次
    runonce(task_id,flag){
        const type="get_user_by_prj"
        this.run_once.visible=true
        this.run_once.type=flag
        this.row_id=task_id
        get_user_byprj(type,task_id).then((response)=>{
            this.userlist=response.data
        })
    },
    //运行（启动、暂停、重启）
    run(task_id,flag){
        if(flag===0){
            this.runonce(task_id,flag)
        }
        else{
        const data={
            "flag":this.status.code,
            "user":this.user,
            "task_id":task_id
        }
        run_route(data).then((response)=>{
            alert(response.message)
            this.run_once.visible=false
            this.showTask()
        })
    }},
    get_map_prj(project){
        let lable=""
        this.options.forEach(item=>{
          if(item.prj_id===project){
              lable=item.prj_name
          }
        })
        return lable
    },
    handleReset() {
        this.pagination = {
          page: 1,
          limit: 5,
          total: 0
        }
        this.queryParams = {
            taskname:undefined,
            project:undefined
        }
        this.showTask()
      },
    handleupdate(row){
         this.resetForm()
         this.dialog = {
          title: '修改任务',
          visible: true,
          type: 'edit'
        }
        const id = row
        detail(id).then(response => {
          this.form = response.data[0].fields
          this.form.task_id=response.data[0].pk
        })
    },
    handleDelete(task_ids) {
        if(this.task_ids.length>0){
          task_ids=this.task_ids
      }
        this.$confirm('确认删除该项目?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          del(task_ids).then(() => {
            this.$message.success('删除成功')
            this.showTask()
          })
        }).catch(() =>
          this.$message.info('已取消删除')
        )
      },
      //添加和编辑的方法
     handleSubmit: function () {
        this.$refs['form'].validate(valid => {
          if (valid) {
            if (this.dialog.type == 'edit') {
              update(this.form.task_id, this.form).then(() => {
                this.$message.success('修改成功')
                this.closeDialog()
                this.showTask()
              })
            } else {
              add(this.form).then(() => {
                this.$message.success('添加成功')
                this.closeDialog()
                this.showTask()
              })
            }
          }
        })
      },
    //列表多选操作
    handleSelectionChange(selection){
        this.task_ids=selection.map(item=>item.pk)
        this.multiple=selection.length === 0
    },
     handleCurrentChange(val) {
      this.pagination.page = val;
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      getTask(this.queryParams).then((response) => {
            this.taskList = response.data.data
            this.pagination.total=response.data.totalCount
      });
    },

  },
  components:{
    
  }

}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }


  ul {
  list-style-type: none;
  padding: 0;
}


li {
  /* display: inline-block; */
  margin: 0 5px;
}


a {
  color: #42b983;
}
</style>



